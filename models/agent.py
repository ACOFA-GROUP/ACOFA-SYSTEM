from sqlalchemy import Column, String, Integer, Date, DateTime, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
import uuid
from database.connection import Base

class Agent(Base):
    __tablename__ = "agents_terrain"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nom_complet = Column(String(200), nullable=False)
    telephone = Column(String(20), nullable=False, unique=True)
    email = Column(String(100), unique=True)
    mot_de_passe_hash = Column(String(255))
    zone_assignee = Column(String(100))
    langue_parlee = Column(String(100), default="Bambara")
    statut = Column(String(20), default="actif")
    nombre_producteurs = Column(Integer, default=0)
    date_embauche = Column(DateTime)
    appareil_mobile = Column(String(100))
    identifiant_appareil = Column(String(200))
    derniere_synchronisation = Column(DateTime)
    date_creation = Column(TIMESTAMP)
    date_modification = Column(TIMESTAMP)
