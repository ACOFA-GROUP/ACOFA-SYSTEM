from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
import models.agent as models
import schemas 
from auth.jwt_handler import create_access_token
from auth.hash_handler import verify_password

router = APIRouter()

@router.post("/agent/login")
def login_agent(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # 1. Recherche de l'agent par email (Image 5 et 14)
    agent = db.query(models.Agent).filter(models.Agent.email == form_data.username).first()
    
    # 2. Vérification du mot de passe (Image 15 pour la colonne mot_de_passe_hash)
    if not agent or not verify_password(form_data.password, agent.mot_de_passe_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 3. Génération du Token
    token_data = {"sub": agent.email, "role": "agent", "user_id": str(agent.id)}
    access_token = create_access_token(data=token_data)
    
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "user_id": agent.id,
        "name": agent.nom_complet
    }

@router.post("/producteur/login")
def login_producteur(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Utilise le modèle Producteur (Image 4)
    import models.producteur as prod_models
    producteur = db.query(prod_models.Producteur).filter(prod_models.Producteur.telephone == form_data.username).first()
    
    if not producteur or str(producteur.code_pin) != str(form_data.password):
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
        "name": producteur.nom
    }
