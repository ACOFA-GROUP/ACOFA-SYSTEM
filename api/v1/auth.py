from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
import models
# On a enlevé l'import de schemas pour éviter les crashs si ce fichier est corrompu
from auth.jwt_handler import create_access_token
from auth.hash_handler import verify_password

router = APIRouter()

@router.post("/agent/login")
def login_agent(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    try:
        # On cherche l'agent
        agent = db.query(models.Agent).filter(models.Agent.email == form_data.username).first()
        
        if not agent or not verify_password(form_data.password, agent.mot_de_passe_hash):
            raise HTTPException(status_code=401, detail="Identifiants incorrects")

        token_data = {"sub": agent.email, "role": "agent", "user_id": str(agent.id)}
        return {
            "access_token": create_access_token(data=token_data), 
            "token_type": "bearer"
        }
    except Exception as e:
        # Ceci affichera l'erreur précise dans les logs sans faire crasher tout le serveur
        raise HTTPException(status_code=500, detail=str(e))
