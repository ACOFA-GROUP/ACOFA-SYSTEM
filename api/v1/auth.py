from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
import models.agent as agent_models
import models.producteur as prod_models
import schemas 
from auth.jwt_handler import create_access_token
from auth.hash_handler import verify_password, get_password_hash

router = APIRouter()

# --- LOGIN AGENT ---
@router.post("/agent/login")
def login_agent(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    agent = db.query(agent_models.Agent).filter(agent_models.Agent.email == form_data.username).first()
    if not agent or not verify_password(form_data.password, agent.mot_de_passe_hash):
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")
    token_data = {"sub": agent.email, "role": "agent", "user_id": str(agent.id)}
    return {
        "access_token": create_access_token(data=token_data), 
        "token_type": "bearer",
        "user_id": agent.id,
        "name": agent.nom_complet
    }

# --- LOGIN PRODUCTEUR (CORRIGÉ POUR ÉVITER L'ERREUR 500) ---
@router.post("/producteur/login")
def login_producteur(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    producteur = db.query(prod_models.Producteur).filter(prod_models.Producteur.telephone == form_data.username).first()
    # Comparaison sécurisée en texte pour éviter le crash
    if not producteur or str(producteur.code_pin) != str(form_data.password):
        raise HTTPException(status_code=401, detail="Téléphone ou code PIN incorrect")
    token_data = {"sub": producteur.telephone, "role": "producteur", "user_id": str(producteur.id)}
    return {
        "access_token": create_access_token(data=token_data), 
        "token_type": "bearer",
        "user_id": producteur.id,
        "name": producteur.nom_complet
    }

# --- REGISTER AGENT (Image 11) ---
@router.post("/agent/register", response_model=schemas.Agent)
def register_agent(agent_in: schemas.AgentCreate, db: Session = Depends(get_db)):
    db_agent = db.query(agent_models.Agent).filter(agent_models.Agent.email == agent_in.email).first()
    if db_agent:
        raise HTTPException(status_code=400, detail="Email déjà utilisé")
    new_agent = agent_models.Agent(
        nom_complet=agent_in.nom_complet,
        email=agent_in.email,
        telephone=agent_in.telephone,
        mot_de_passe_hash=get_password_hash(agent_in.password),
        is_active=True
    )
    db.add(new_agent)
    db.commit()
    db.refresh(new_agent)
    return new_agent

# --- REGISTER PRODUCTEUR (Image 13) ---
@router.post("/producteur/register", response_model=schemas.Producteur)
def register_producteur(prod_in: schemas.ProducteurCreate, db: Session = Depends(get_db)):
    db_prod = db.query(prod_models.Producteur).filter(prod_models.Producteur.telephone == prod_in.telephone).first()
    if db_prod:
        raise HTTPException(status_code=400, detail="Téléphone déjà utilisé")
    new_prod = prod_models.Producteur(
        nom_complet=prod_in.nom_complet,
        telephone=prod_in.telephone,
        code_pin=prod_in.code_pin,
        localite=prod_in.localite,
        cooperative_id=prod_in.cooperative_id
    )
    db.add(new_prod)
    db.commit()
    db.refresh(new_prod)
    return new_prod
