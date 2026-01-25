from pydantic import BaseModel, EmailStr

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
