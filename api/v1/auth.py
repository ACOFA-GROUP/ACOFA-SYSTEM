from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database.connection import get_db  # adapte si chez toi c'est database import get_db
from schemas.auth import TokenResponse  # ton schema TokenResponse
from models.agent import Agent
from models.producteur import Producteur
from auth.jwt_handler import create_access_token
from auth.password import verify_password  # verify_password(password_plain, hashed)

router = APIRouter()

# -------------------------
# LOGIN AGENT (Swagger: username=email, password=motdepasse)
# -------------------------
@router.post("/agent/login", response_model=TokenResponse)
async def agent_login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # Swagger envoie: username + password
    agent = db.query(Agent).filter(Agent.email == form_data.username).first()

    if not agent or not verify_password(form_data.password, agent.mot_de_passe_hash):
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


# -------------------------
# LOGIN PRODUCTEUR (Swagger: username=telephone, password=code_pin)
# -------------------------
@router.post("/producteur/login", response_model=TokenResponse)
async def producteur_login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # username = telephone, password = code_pin
    producteur = db.query(Producteur).filter(Producteur.telephone == form_data.username).first()

    if not producteur:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Téléphone ou code PIN incorrect"
        )

    # Comparaison safe en string
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
