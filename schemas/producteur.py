from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProducteurBase(BaseModel):
    nom_complet: str
    sexe: str
    telephone: str
    village: Optional[str] = None
    localite: str
    commune_cercle: str
    region: str
    latitude: float
    longitude: float
    cooperative_nom: Optional[str] = None
    langue_preferee: str = "bambara"

class ProducteurCreate(ProducteurBase):
    agent_enregistrement_id: str
    age_approximatif: Optional[int] = None
    telephone_secondaire: Optional[str] = None

class ProducteurResponse(ProducteurBase):
    id: str
    date_enregistrement: datetime
    statut: str
    
    class Config:
        from_attributes = True
