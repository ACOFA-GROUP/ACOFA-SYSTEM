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
    # On cherche l'agent par l'email saisi dans le champ 'username' de Swagger
    agent = db.query(models.Agent).filter(models.Agent.email == form_data.username).first()
    
    # Correction cruciale : on utilise 'mot_de_passe_hash' (vu dans ta table Supabase)
    if not agent or not verify_password(form_data.password, agent.mot_de_passe_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Création du token sécurisé
    token_data = {"sub": agent.email, "role": "agent", "user_id": str(agent.id)}
    access_token = create_access_token(data=token_data)
    
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "user_id": agent.id,
        "role": "agent",
        "name": agent.nom_complet if hasattr(agent, 'nom_complet') else "Agent"
    }

@router.post("/producteur/login")
def login_producteur(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Pour le producteur, on utilise le téléphone saisi dans le champ 'username'
    producteur = db.query(models.Producteur).filter(models.Producteur.telephone == form_data.username).first()
    
    # Vérification du code PIN (vérifie que la colonne s'appelle bien code_pin dans ta table producteurs)
    if not producteur or producteur.code_pin != form_data.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Téléphone ou code PIN incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token_data = {"sub": producteur.telephone, "role": "producteur", "user_id": str(producteur.id)}
    access_token = create_access_token(data=token_data)

    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "user_id": producteur.id,
        "role": "producteur",
        "name": producteur.nom if hasattr(producteur, 'nom') else "Producteur"
    }
