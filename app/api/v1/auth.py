from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.schemas.auth import AgentLogin, ProducteurLogin, TokenResponse
from app.models.agent import Agent
from app.models.producteur import Producteur
from app.auth.jwt_handler import create_access_token
from app.auth.password import verify_password
from app.auth.dependencies import get_current_user

router = APIRouter()

@router.post("/agent/login", response_model=TokenResponse)
async def agent_login(credentials: AgentLogin, db: Session = Depends(get_db)):
    """
    Login pour agents ACOFA
    - Email + Password
    - Retourne JWT token
    """
    # Récupérer agent depuis DB
    agent = db.query(Agent).filter(Agent.email == credentials.email).first()
    
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect"
        )
    
    # Vérifier mot de passe
    if not agent.mot_de_passe_hash or not verify_password(credentials.password, agent.mot_de_passe_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect"
        )
    
    # Créer token JWT
    token_data = {
        "user_id": str(agent.id),
        "role": "agent",
        "email": agent.email,
        "name": agent.nom_complet
    }
    
    token = create_access_token(token_data)
    
    return TokenResponse(
        access_token=token,
        user_id=str(agent.id),
        role="agent",
        name=agent.nom_complet
    )

@router.post("/producteur/login", response_model=TokenResponse)
async def producteur_login(credentials: ProducteurLogin, db: Session = Depends(get_db)):
    """
    Login pour producteurs
    - Téléphone + Code PIN (6 chiffres)
    - Retourne JWT token
    """
    # Récupérer producteur depuis DB
    producteur = db.query(Producteur).filter(
        Producteur.telephone == credentials.telephone
    ).first()
    
    if not producteur:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Téléphone ou code PIN incorrect"
        )
    
    # Vérifier code PIN
    if not producteur.code_pin or producteur.code_pin != credentials.code_pin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Téléphone ou code PIN incorrect"
        )
    
    # Créer token JWT
    token_data = {
        "user_id": str(producteur.id),
        "role": "producteur",
        "telephone": producteur.telephone,
        "name": producteur.nom_complet
    }
    
    token = create_access_token(token_data)
    
    return TokenResponse(
        access_token=token,
        user_id=str(producteur.id),
        role="producteur",
        name=producteur.nom_complet
    )

@router.get("/verify")
async def verify_token(current_user: dict = Depends(get_current_user)):
    """
    Vérifier si le token est valide
    """
    return {
        "valid": True,
        "user_id": current_user["user_id"],
        "role": current_user["role"]
    }
