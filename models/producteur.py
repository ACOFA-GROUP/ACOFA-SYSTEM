from sqlalchemy import Column, String, Integer, Boolean, Float, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from geoalchemy2 import Geography
import uuid
from app.database.connection import Base

class Producteur(Base):
    __tablename__ = "producteurs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nom_complet = Column(String(200), nullable=False)
    sexe = Column(String(10), nullable=False)
    age_approximatif = Column(Integer)
    telephone = Column(String(20), nullable=False, unique=True)
    telephone_secondaire = Column(String(20))
    code_pin = Column(String(6))
    derniere_connexion = Column(DateTime)
    village = Column(String(100))
    localite = Column(String(100), nullable=False)
    commune_cercle = Column(String(100), nullable=False)
    region = Column(String(50), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    altitude = Column(Float)
    precision_gps = Column(Float)
    point_gps = Column(Geography('POINT', srid=4326))
    cooperative_nom = Column(String(200))
    niveau_etudes = Column(String(50))
    langue_preferee = Column(String(50), default="bambara")
    personnes_foyer = Column(Integer)
    personnes_disponibles_champs = Column(Integer)
    source_revenu_autre = Column(Boolean, default=False)
    souhaite_appui_technique = Column(Boolean, default=False)
    souhaite_contrat_acofa = Column(Boolean, default=False)
    peut_livrer_seul = Column(Boolean, default=False)
    partage_espace_materiel = Column(Boolean, default=False)
    souhaite_etre_recontacte = Column(Boolean, default=True)
    distance_marche_km = Column(Float)
    agent_enregistrement_id = Column(UUID(as_uuid=True), ForeignKey('agents_terrain.id'))
    date_enregistrement = Column(DateTime, server_default=func.now())
    date_modification = Column(DateTime, server_default=func.now(), onupdate=func.now())
    statut = Column(String(20), default="actif")
