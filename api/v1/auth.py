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
    # On cherche dynamiquement le modèle Agent ou AgentTerrain
    agent_model = getattr(models, "Agent", getattr(models, "AgentTerrain", None))
    
    if agent_model is None:
        raise HTTPException(status_code=500, detail="Erreur interne : Modèle Agent introuvable")

    # Recherche par email (dans le champ username de Swagger)
    agent = db.query(agent_model).filter(agent_model.email == form_data.username).first()
    
    # Vérification avec la colonne de ta base Supabase : mot_de_passe_hash
    # On vérifie si l'agent existe et si le mot de passe correspond
    if not agent:
        raise HTTPException(status_code=401, detail="Email incorrect")
    
    # On vérifie dynamiquement si la colonne s'appelle password ou mot_de_passe_hash
    stored_password = getattr(agent, "mot_de_passe_hash", getattr(agent, "password", None))
    
    if not stored_password or not verify_password(form_data.password, stored_password):
        raise HTTPException(status_code=401, detail="Mot de passe incorrect")

    # Génération du Token
    token_data = {"sub": agent.email, "role": "agent", "user_id": str(agent.id)}
    access_token = create_access_token(data=token_data)
    
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "user_id": agent.id,
        "role": "agent"
    }

@router.post("/producteur/login")
def login_producteur(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Recherche du producteur par téléphone
    producteur = db.query(models.Producteur).filter(models.Producteur.telephone == form_data.username).first()
    
    # Comparaison directe du code PIN
    if not producteur or str(producteur.code_pin) != str(form_data.password):
        raise HTTPException(status_code=401, detail="Téléphone ou code PIN incorrect")

    token_data = {"sub": producteur.telephone, "role": "producteur", "user_id": str(producteur.id)}
    access_token = create_access_token(data=token_data)

    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "user_id": producteur.id,
        "role": "producteur"
    }
