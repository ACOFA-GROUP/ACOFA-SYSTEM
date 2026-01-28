from pydantic import BaseModel


class AgentLogin(BaseModel):
    username: str
    password: str


class ProducteurLogin(BaseModel):
    telephone: str
    code_pin: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str
    role: str
    name: str = ""   # ✅ évite le crash si name est None
