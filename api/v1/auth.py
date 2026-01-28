from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.connection import get_db
from schemas.auth import AgentLogin, ProducteurLogin, TokenResponse
from models.agent import Agent
from models.producteur import Producteur
from auth.jwt_handler import create_access_token
from auth.password import verify_password

router = APIRouter()


@router.post("/agent/login", response_model=TokenResponse)
async def agent_login(credentials: AgentLogin, db: Session = Depends(get_db)):
    # On cherche l'agent par username (chez toi: c'est l'email)
    agent = db.query(Agent).filter(Agent.email == credentials.username).first()

    if not agent:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect"
        )

    # Vérif mot de passe (bcrypt)
    if not agent.mot_de_passe_hash or not verify_password(credentials.password, agent.mot_de_passe_hash):
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
async def producteur_login(credentials: ProducteurLogin, db: Session = Depends(get_db)):
    producteur = db.query(Producteur).filter(Producteur.telephone == credentials.telephone).first()

    if not producteur:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Téléphone ou code PIN incorrect"
        )

    # Comparaison PIN en texte (évite bug int/str)
    if producteur.code_pin is None or str(producteur.code_pin) != str(credentials.code_pin):
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
