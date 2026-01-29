from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from database.connection import get_db
from models.agent import Agent
from models.producteur import Producteur
from auth.jwt_handler import create_access_token
from auth.password import verify_password

router = APIRouter()


async def read_credentials(request: Request):
    """
    Accepte:
    - FORM: application/x-www-form-urlencoded (Swagger avec OAuth2 form)
    - JSON: application/json
    Retourne dict avec username/password (ou telephone/code_pin)
    """
    content_type = (request.headers.get("content-type") or "").lower()

    # JSON
    if "application/json" in content_type:
        data = await request.json()
        return data if isinstance(data, dict) else {}

    # FORM
    form = await request.form()
    return dict(form)


@router.post("/agent/login")
async def login_agent(request: Request, db: Session = Depends(get_db)):
    data = await read_credentials(request)

    # Support JSON: {username, password}
    # Support FORM: {username, password}
    username = data.get("username") or data.get("email")
    password = data.get("password")

    if not username or not password:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Champs requis: username et password"
        )

    agent = db.query(Agent).filter(Agent.email == str(username)).first()

    if not agent or not verify_password(str(password), agent.mot_de_passe_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect"
        )

    token_data = {"user_id": str(agent.id), "role": "agent", "name": agent.nom_complet}
    token = create_access_token(token_data)

    return {
        "access_token": token,
        "token_type": "bearer",
        "user_id": str(agent.id),
        "role": "agent",
        "name": agent.nom_complet or agent.email or "Agent"
    }


@router.post("/producteur/login")
async def login_producteur(request: Request, db: Session = Depends(get_db)):
    data = await read_credentials(request)

    # Support JSON: {telephone, code_pin}
    telephone = data.get("telephone")

    # Support FORM: username=password fields (comme OAuth2)
    # ex: username=70000000, password=1234
    if telephone is None:
        telephone = data.get("username")

    code_pin = data.get("code_pin")
    if code_pin is None:
        code_pin = data.get("password")

    if not telephone or code_pin is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Champs requis: telephone+code_pin (JSON) ou username+password (FORM)"
        )

    producteur = db.query(Producteur).filter(Producteur.telephone == str(telephone)).first()

    if not producteur:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Téléphone ou code PIN incorrect"
        )

    if producteur.code_pin is None or str(producteur.code_pin) != str(code_pin):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Téléphone ou code PIN incorrect"
        )

    token_data = {"user_id": str(producteur.id), "role": "producteur", "name": producteur.nom_complet}
    token = create_access_token(token_data)

    return {
        "access_token": token,
        "token_type": "bearer",
        "user_id": str(producteur.id),
        "role": "producteur",
        "name": producteur.nom_complet or producteur.telephone or "Producteur"
    }
