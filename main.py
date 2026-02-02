"""
ACOFA AGROLINK - Backend API Minimal
Version: 1.0 MVP (Login fonctionnel)
"""

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta
from jose import jwt
import os

# ============================================================================
# CONFIGURATION
# ============================================================================

app = FastAPI(
    title="ACOFA AGROLINK API",
    description="API pour la gestion agricole intelligente",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuration JWT
JWT_SECRET = os.getenv("JWT_SECRET", "votre-secret-key-change-en-production")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_MINUTES = 10080  # 7 jours

# ============================================================================
# CORS - IMPORTANT pour Vercel
# ============================================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://v0-acofa-agrolink-build.vercel.app",
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# SCHEMAS
# ============================================================================

class AgentLogin(BaseModel):
    email: EmailStr
    password: str

class ProducteurLogin(BaseModel):
    telephone: str
    code_pin: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str
    role: str
    name: str

# ============================================================================
# FONCTIONS UTILITAIRES
# ============================================================================

def create_access_token(data: dict):
    """Créer un token JWT"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=JWT_EXPIRATION_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt

# ============================================================================
# ROUTES
# ============================================================================

@app.get("/")
async def root():
    """Page d'accueil API"""
    return {
        "message": "ACOFA AGROLINK API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check pour Railway"""
    return {"status": "healthy"}

@app.post("/api/v1/auth/agent/login", response_model=TokenResponse)
async def agent_login(credentials: AgentLogin):
    """
    Login pour agents ACOFA
    - Email + Password
    - Retourne JWT token
    
    Identifiants de test:
    - Email: agent@acofa.com
    - Password: Acofa123
    """
    # Vérification des identifiants
    if credentials.email == "agent@acofa.com" and credentials.password == "Acofa123":
        token_data = {
            "user_id": "agent-uuid-123",
            "role": "agent",
            "email": credentials.email,
            "name": "Amadou Traoré"
        }
        token = create_access_token(token_data)
        
        return TokenResponse(
            access_token=token,
            user_id=token_data["user_id"],
            role="agent",
            name=token_data["name"]
        )
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials"
    )

@app.post("/api/v1/auth/producteur/login", response_model=TokenResponse)
async def producteur_login(credentials: ProducteurLogin):
    """
    Login pour producteurs
    - Téléphone + Code PIN
    - Retourne JWT token
    
    Identifiants de test:
    - Téléphone: +223 70 00 00 01
    - Code PIN: 123456
    """
    if credentials.telephone == "+223 70 00 00 01" and credentials.code_pin == "123456":
        token_data = {
            "user_id": "producteur-uuid-456",
            "role": "producteur",
            "telephone": credentials.telephone,
            "name": "Moussa Diarra"
        }
        token = create_access_token(token_data)
        
        return TokenResponse(
            access_token=token,
            user_id=token_data["user_id"],
            role="producteur",
            name=token_data["name"]
        )
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials"
    )

# ============================================================================
# DÉMARRAGE
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
