from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm # Ajouté pour fixer 422
from sqlalchemy.orm import Session

from database.connection import get_db
from schemas.auth import TokenResponse
from models.agent import Agent
from models.producteur import Producteur
from auth.jwt_handler import create_access_token
from auth.password import verify_password

router = APIRouter()

@router.post("/agent/login", response_model=TokenResponse)
async def agent_login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # On utilise form_data.username (Email dans Swagger)
    agent = db.query(Agent).filter(Agent.email == form_data.username).first()

    if not agent:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect"
        )

    if not agent.mot_de_passe_hash or not verify_password(form_data.password, agent.mot_de_passe_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect"
        )

    token_data = {
        "user_id": str(agent.id),
        "role": "agent",
        "email": agent.email,
        "name": agent.nom_complet
    }

    token = create_access_token(token_data)

    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user_id=str(agent.id),
        role="agent",
        name=agent.nom_complet
    )

@router.post("/producteur/login", response_model=TokenResponse)
async def producteur_login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # form_data.username contient le téléphone dans Swagger
    producteur = db.query(Producteur).filter(Producteur.telephone == form_data.username).first()

    if not producteur:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Téléphone ou code PIN incorrect"
        )

    # Comparaison PIN (form_data.password contient le PIN dans Swagger)
    if producteur.code_pin is None or str(producteur.code_pin) != str(form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Téléphone ou code PIN incorrect"
        )

    token_data = {
        "user_id": str(producteur.id),
        "role": "producteur",
        "telephone": producteur.telephone,
        "name": producteur.nom_complet
    }

    token = create_access_token(token_data)

    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user_id=str(producteur.id),
        role="producteur",
        name=producteur.nom_complet
    )
