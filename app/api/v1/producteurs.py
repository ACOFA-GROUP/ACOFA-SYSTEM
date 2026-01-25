from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from app.database.connection import get_db
from app.schemas.producteur import ProducteurCreate, ProducteurResponse
from app.models.producteur import Producteur
from app.auth.dependencies import get_current_user, require_agent

router = APIRouter()

@router.post("/", response_model=ProducteurResponse, status_code=status.HTTP_201_CREATED)
async def create_producteur(
    producteur: ProducteurCreate,
    db: Session = Depends(get_db),
    current_agent: dict = Depends(require_agent)
):
    existing = db.query(Producteur).filter(Producteur.telephone == producteur.telephone).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Un producteur avec ce numéro existe déjà"
        )
    
    point_gps = f"SRID=4326;POINT({producteur.longitude} {producteur.latitude})"
    
    new_producteur = Producteur(
        nom_complet=producteur.nom_complet,
        sexe=producteur.sexe,
        telephone=producteur.telephone,
        telephone_secondaire=producteur.telephone_secondaire,
        age_approximatif=producteur.age_approximatif,
        village=producteur.village,
        localite=producteur.localite,
        commune_cercle=producteur.commune_cercle,
        region=producteur.region,
        latitude=producteur.latitude,
        longitude=producteur.longitude,
        point_gps=point_gps,
        cooperative_nom=producteur.cooperative_nom,
        langue_preferee=producteur.langue_preferee,
        agent_enregistrement_id=UUID(producteur.agent_enregistrement_id)
    )
    
    db.add(new_producteur)
    db.commit()
    db.refresh(new_producteur)
    
    return new_producteur

@router.get("/", response_model=List[ProducteurResponse])
async def list_producteurs(
    skip: int = 0,
    limit: int = 100,
    region: str = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    query = db.query(Producteur)
    if region:
        query = query.filter(Producteur.region == region)
    if current_user.get("role") == "agent":
        query = query.filter(Producteur.agent_enregistrement_id == UUID(current_user["user_id"]))
    
    producteurs = query.offset(skip).limit(limit).all()
    return producteurs

@router.get("/{producteur_id}", response_model=ProducteurResponse)
async def get_producteur(
    producteur_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    producteur = db.query(Producteur).filter(Producteur.id == UUID(producteur_id)).first()
    if not producteur:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producteur non trouvé")
    return producteur
