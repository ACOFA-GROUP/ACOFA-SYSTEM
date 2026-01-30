from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

from database.connection import get_db
from schemas.auth import TokenResponse
from models.agent import Agent
from models.producteur import Producteur
from auth.jwt_handler import create_access_token
from auth.password import verify_password

router = APIRouter()


# =========================
# SCHEMA LOGIN JSON (AGENT)
# =========================
class LoginRequest(BaseModel):
    username: str
    password: str


# =========================
# LOGIN AGENT (JSON)
# =========================
@router.post("/agent/login", response_model=TokenResponse)
async def agent_login(
    credentials: LoginRequest,
    db: Session = Depends(get_db)
):
    agent = (
        db.query(Agent)
        .filter(Agent.email == credentials.username)
        .first()
    )

    if not agent or not verify_password(credentials.password, agent.mot_de_passe_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect"
        )

    token_data = {
        "user_id": str(agent.id),
        "role": "agent",
        "name": agent.nom_complet
    }

    return TokenResponse(
        access_token=create_access_token(token_data),
        token_type="bearer",
        user_id=str(agent.id),
        role="agent",
        name=agent.nom_complet
    )


# =========================
# LOGIN PRODUCTEUR (INCHANGÉ – FORM DATA)
# =========================
@router.post("/producteur/login", response_model=TokenResponse)
async def producteur_login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    producteur = (
        db.query(Producteur)
        .filter(Producteur.telephone == form_data.username)
        .first()
    )

    if not producteur:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Téléphone ou code PIN incorrect"
        )

    if producteur.code_pin is None or str(producteur.code_pin) != str(form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Téléphone ou code PIN incorrect"
        )

    token_data = {
        "user_id": str(producteur.id),
        "role": "producteur",
        "name": producteur.nom_complet
    }

    return TokenResponse(
        access_token=create_access_token(token_data),
        token_type="bearer",
        user_id=str(producteur.id),
        role="producteur",
        name=producteur.nom_complet
    )
