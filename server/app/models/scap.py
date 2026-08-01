from sqlalchemy import Column, Integer, String, Text
from app.db.base_class import Base

class ScapMetadata(Base):
    __tablename__ = "scap_metadata"

    id = Column(Integer, primary_key=True, index=True)
    rule_id = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    severity = Column(String, nullable=False)
    description = Column(Text)
    rationale = Column(Text)
