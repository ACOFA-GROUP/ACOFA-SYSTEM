from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.orm import Session
from database.connection import get_db
from schemas.auth import AgentLogin, ProducteurLogin, TokenResponse
from models.agent import Agent
from models.producteur import Producteur
from auth.jwt_handler import create_access_token
from auth.password import verify_password
from auth.dependencies import get_current_user

router = APIRouter()

@router.post("/agent/login", response_model=TokenResponse)
async def agent_login(credentials: AgentLogin, db: Session = Depends(get_db)):
    agent = db.query(Agent).filter(Agent.email == credentials.username).first()
    if not agent:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email ou mot de passe incorrect")
    
    if not agent.mot_de_passe_hash or not verify_password(credentials.password, agent.mot_de_passe_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email ou mot de passe incorrect")
    
    token_data = {"user_id": str(agent.id), "role": "agent", "email": agent.email, "name": agent.nom_complet}
    token = create_access_token(token_data)
    return TokenResponse(access_token=token, user_id=str(agent.id), role="agent", name=agent.nom_complet)

@router.post("/producteur/login", response_model=TokenResponse)
async def producteur_login(credentials: ProducteurLogin, db: Session = Depends(get_db)):
    producteur = db.query(Producteur).filter(Producteur.telephone == credentials.telephone).first()
    if not producteur:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Téléphone ou code PIN incorrect")
    
    if not producteur.code_pin or producteur.code_pin != credentials.code_pin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Téléphone ou code PIN incorrect")
    
    token_data = {"user_id": str(producteur.id), "role": "producteur", "telephone": producteur.telephone, "name": producteur.nom_complet}
    token = create_access_token(token_data)
    return TokenResponse(access_token=token, user_id=str(producteur.id), role="producteur", name=producteur.nom_complet)

@router.get("/verify")
async def verify_token(current_user: dict = Depends(get_current_user)):
    return {"valid": True, "user_id": current_user["user_id"], "role": current_user["role"]}

@router.get("/debug/db")
def debug_db(db: Session = Depends(get_db)):
    # CORRECTION ICI : Ajout de text()
    result = db.execute(text("SELECT current_database(), current_schema()")).fetchone()
    return {
        "database": result[0],
        "schema": result[1]
    }
