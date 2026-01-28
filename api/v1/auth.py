from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
import models.agent as models 
import schemas  # Importation corrigée selon ton dossier
from auth.jwt_handler import create_access_token
from auth.hash_handler import verify_password

router = APIRouter()

@router.post("/agent/login")
def login_agent(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # On cherche l'agent (Modèle Agent, colonne email)
    agent = db.query(models.Agent).filter(models.Agent.email == form_data.username).first()
    
    # Vérification avec mot_de_passe_hash (vu sur ta photo Supabase)
    if not agent or not verify_password(form_data.password, agent.mot_de_passe_hash):
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")

    token_data = {"sub": agent.email, "role": "agent", "user_id": str(agent.id)}
    return {
        "access_token": create_access_token(data=token_data), 
        "token_type": "bearer",
        "user_id": agent.id,
        "name": agent.nom_complet
    }
