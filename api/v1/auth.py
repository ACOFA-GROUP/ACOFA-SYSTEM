from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, load_only
from pydantic import BaseModel

from database.connection import get_db
from schemas.auth import TokenResponse
from models.agent import Agent
from models.producteur import Producteur
from auth.jwt_handler import create_access_token
from auth.password import verify_password

router = APIRouter()


# =========================
# SCHEMA LOGIN (STANDARD)
# =========================
class LoginRequest(BaseModel):
    username: str
    password: str


# =========================
# LOGIN AGENT
# username = email
# password = mot de passe
# =========================
@router.post("/agent/login", response_model=TokenResponse)
async def agent_login(
    credentials: LoginRequest,
    db: Session = Depends(get_db),
):
    agent = db.query(Agent).filter(
        Agent.email == credentials.username
    ).first()

    if not agent or not verify_password(
        credentials.password,
        agent.mot_de_passe_hash
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect",
        )

    token_data = {
        "user_id": str(agent.id),
        "role": "agent",
        "name": agent.nom_complet,
    }

    return TokenResponse(
        access_token=create_access_token(token_data),
        token_type="bearer",
        user_id=str(agent.id),
        role="agent",
        name=agent.nom_complet,
    )


# =========================
# LOGIN PRODUCTEUR
# username = telephone
# password = code PIN
# =========================
@router.post("/producteur/login", response_model=TokenResponse)
async def producteur_login(
    credentials: LoginRequest,
    db: Session = Depends(get_db),
):
    try:
        # ✅ IMPORTANT: on charge uniquement les colonnes nécessaires
        producteur = (
            db.query(Producteur)
            .options(
                load_only(
                    Producteur.id,
                    Producteur.telephone,
                    Producteur.code_pin,
                    Producteur.nom_complet
                )
            )
            .filter(Producteur.telephone == credentials.username)
            .first()
        )

        if not producteur:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Téléphone ou code PIN incorrect",
            )

        if producteur.code_pin is None or str(producteur.code_pin) != str(credentials.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Téléphone ou code PIN incorrect",
            )

        name = producteur.nom_complet if getattr(producteur, "nom_complet", None) else "Producteur"

        token_data = {
            "user_id": str(producteur.id),
            "role": "producteur",
            "name": name,
        }

        return TokenResponse(
            access_token=create_access_token(token_data),
            token_type="bearer",
            user_id=str(producteur.id),
            role="producteur",
            name=name,
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur producteur_login: {type(e).__name__}: {str(e)}",
        )
