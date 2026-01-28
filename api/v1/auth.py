from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import logging

from database.connection import get_db
from schemas.auth import AgentLogin, ProducteurLogin, TokenResponse
from models.agent import Agent
from models.producteur import Producteur
from auth.jwt_handler import create_access_token
from auth.password import verify_password

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/agent/login", response_model=TokenResponse)
async def agent_login(credentials: AgentLogin, db: Session = Depends(get_db)):
    try:
        agent = db.query(Agent).filter(Agent.email == credentials.username).first()

        if not agent:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email ou mot de passe incorrect"
            )

        if not agent.mot_de_passe_hash or not verify_password(credentials.password, agent.mot_de_passe_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email ou mot de passe incorrect"
            )

        token_data = {
            "user_id": str(agent.id),
            "role": "agent",
            "email": agent.email,
            "name": agent.nom_complet or "Agent"
        }

        token = create_access_token(token_data)

        return TokenResponse(
            access_token=str(token),
            token_type="bearer",
            user_id=str(agent.id),
            role="agent",
            name=agent.nom_complet or "Agent"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("CRASH agent_login: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur interne serveur (agent_login)"
        )


@router.post("/producteur/login", response_model=TokenResponse)
async def producteur_login(credentials: ProducteurLogin, db: Session = Depends(get_db)):
    try:
        producteur = (
            db.query(Producteur)
            .filter(Producteur.telephone == credentials.telephone)
            .first()
        )

        if not producteur:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Téléphone ou code PIN incorrect"
            )

        # IMPORTANT : éviter None + comparaison sûre
        db_pin = "" if producteur.code_pin is None else str(producteur.code_pin).strip()
        req_pin = "" if credentials.code_pin is None else str(credentials.code_pin).strip()

        if db_pin == "" or db_pin != req_pin:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Téléphone ou code PIN incorrect"
            )

        # IMPORTANT : éviter que "name" soit None => ResponseValidationError => 500
        safe_name = (producteur.nom_complet or "Producteur").strip() or "Producteur"

        token_data = {
            "user_id": str(producteur.id),
            "role": "producteur",
            "telephone": str(producteur.telephone or ""),
            "name": safe_name
        }

        token = create_access_token(token_data)

        return TokenResponse(
            access_token=str(token),
            token_type="bearer",
            user_id=str(producteur.id),
            role="producteur",
            name=safe_name
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("CRASH producteur_login: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur interne serveur (producteur_login)"
        )


@router.get("/verify")
async def verify_token(current_user: dict = Depends(lambda: {})):
    # (optionnel, tu peux garder ta version)
    return {"valid": True}
