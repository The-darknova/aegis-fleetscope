from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base_class import Base


class ComplianceScore(Base):
    __tablename__ = "compliance_scores"

    id = Column(Integer, primary_key=True, index=True)
    host_id = Column(Integer, ForeignKey("hosts.id"), nullable=False)
    policy_id = Column(Integer, ForeignKey("policies.id"), nullable=False)
    score = Column(Float, nullable=False) # Percentage or similar metric
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    host = relationship("Host", back_populates="compliance_scores")
    policy = relationship("Policy", back_populates="compliance_scores")
