from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
import models
import schemas
from auth.jwt_handler import create_access_token
from auth.hash_handler import verify_password

router = APIRouter()

@router.post("/agent/login")
def login_agent(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # On cherche l'agent dans la table 'agents_terrain' (via le modèle Agent)
    agent = db.query(models.Agent).filter(models.Agent.email == form_data.username).first()
    
    if not agent:
        raise HTTPException(status_code=401, detail="Email inconnu")

    # On utilise le nom exact de ta colonne Supabase
    if not verify_password(form_data.password, agent.mot_de_passe_hash):
        raise HTTPException(status_code=401, detail="Mot de passe incorrect")

    token_data = {"sub": agent.email, "role": "agent", "user_id": str(agent.id)}
    return {
        "access_token": create_access_token(data=token_data), 
        "token_type": "bearer"
    }

@router.post("/producteur/login")
def login_producteur(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    producteur = db.query(models.Producteur).filter(models.Producteur.telephone == form_data.username).first()
    
    if not producteur or str(producteur.code_pin) != str(form_data.password):
        raise HTTPException(status_code=401, detail="Identifiants invalides")

    token_data = {"sub": producteur.telephone, "role": "producteur", "user_id": str(producteur.id)}
    return {
        "access_token": create_access_token(data=token_data), 
        "token_type": "bearer"
    }
