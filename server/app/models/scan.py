from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base_class import Base


class HistoricalScan(Base):
    __tablename__ = "historical_scans"

    id = Column(Integer, primary_key=True, index=True)
    host_id = Column(Integer, ForeignKey("hosts.id"), nullable=False)
    policy_id = Column(Integer, ForeignKey("policies.id"), nullable=False)
    scan_time = Column(DateTime(timezone=True), server_default=func.now())
    
    passed_rules = Column(Integer, default=0)
    failed_rules = Column(Integer, default=0)
    total_rules = Column(Integer, default=0)
    
    # Raw XML result could be stored here or in GCS/S3
    raw_report_xml = Column(Text) 

    host = relationship("Host", back_populates="scans")
    policy = relationship("Policy", back_populates="scans")
