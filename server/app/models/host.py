from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base_class import Base


class Host(Base):
    __tablename__ = "hosts"

    id = Column(Integer, primary_key=True, index=True)
    hostname = Column(String, index=True, nullable=False)
    ip_address = Column(String, nullable=False)
    os_name = Column(String, nullable=False)  # e.g., Ubuntu, RHEL
    os_version = Column(String, nullable=False)
    architecture = Column(String, nullable=False)
    last_seen = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    is_active = Column(Boolean, default=True)

    scans = relationship("HistoricalScan", back_populates="host")
    compliance_scores = relationship("ComplianceScore", back_populates="host")
