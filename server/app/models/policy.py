from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Policy(Base):
    __tablename__ = "policies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String)
    is_active = Column(Boolean, default=True)
    scap_profile = Column(String, nullable=False) # e.g. xccdf_org.ssgproject.content_profile_standard

    scans = relationship("HistoricalScan", back_populates="policy")
    compliance_scores = relationship("ComplianceScore", back_populates="policy")
