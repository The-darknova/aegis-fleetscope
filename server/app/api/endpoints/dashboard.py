from typing import List, Optional
from pydantic import BaseModel

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db.session import get_db
from app.models.host import Host
from app.models.policy import Policy
from app.models.scan import HistoricalScan
from app.models.compliance import ComplianceScore
from app.core.security import get_current_admin

router = APIRouter()

# -- Dashboard Agents APIs --
@router.get("/agents")
async def list_agents(db: Session = Depends(get_db), admin: str = Depends(get_current_admin)):
    hosts = db.query(Host).all()
    result = []
    for h in hosts:
        result.append({
            "id": str(h.id),
            "hostname": h.hostname,
            "os_name": h.os_name,
            "os_version": h.os_version,
            "architecture": h.architecture,
            "last_seen": h.last_seen.isoformat() if h.last_seen else None
        })
    return result

@router.get("/agents/{agent_id}")
async def get_agent(agent_id: int, db: Session = Depends(get_db), admin: str = Depends(get_current_admin)):
    h = db.query(Host).filter(Host.id == agent_id).first()
    if not h:
        raise HTTPException(status_code=404, detail="Agent not found")
    return {
        "id": str(h.id),
        "hostname": h.hostname,
        "os_name": h.os_name,
        "os_version": h.os_version,
        "architecture": h.architecture,
        "last_seen": h.last_seen.isoformat() if h.last_seen else None
    }

# -- Dashboard Compliance APIs --
@router.get("/compliance/overview")
async def get_compliance_overview(db: Session = Depends(get_db), admin: str = Depends(get_current_admin)):
    total_agents = db.query(Host).count()
    
    # Very simple logic for beta
    scores = db.query(ComplianceScore).all()
    
    if not scores:
        return {
            "total_agents": total_agents,
            "compliant_agents": 0,
            "non_compliant_agents": 0,
            "average_score": 0.0
        }
        
    total_score = sum(s.score for s in scores)
    avg_score = total_score / len(scores)
    
    # Just a mock grouping for beta
    compliant = sum(1 for s in scores if s.score >= 90)
    non_compliant = len(scores) - compliant
    
    # Distinct hosts that have reported
    return {
        "total_agents": total_agents,
        "compliant_agents": compliant,
        "non_compliant_agents": non_compliant,
        "average_score": avg_score
    }

@router.get("/compliance/reports")
async def list_reports(db: Session = Depends(get_db), admin: str = Depends(get_current_admin)):
    scans = db.query(HistoricalScan).order_by(HistoricalScan.scan_time.desc()).all()
    result = []
    for s in scans:
        # Get the corresponding score
        score = db.query(ComplianceScore).filter(
            ComplianceScore.host_id == s.host_id,
            ComplianceScore.policy_id == s.policy_id
        ).order_by(ComplianceScore.timestamp.desc()).first()
        
        result.append({
            "id": str(s.id),
            "agent_id": str(s.host_id),
            "timestamp": s.scan_time.isoformat() if s.scan_time else None,
            "score": score.score if score else 0
        })
    return result

@router.get("/compliance/reports/{report_id}")
async def get_report_details(report_id: int, db: Session = Depends(get_db), admin: str = Depends(get_current_admin)):
    scan = db.query(HistoricalScan).filter(HistoricalScan.id == report_id).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Report not found")
        
    score = db.query(ComplianceScore).filter(
        ComplianceScore.host_id == scan.host_id,
        ComplianceScore.policy_id == scan.policy_id
    ).order_by(ComplianceScore.timestamp.desc()).first()
    
    return {
        "id": str(scan.id),
        "summary": {
            "id": str(scan.id),
            "agent_id": str(scan.host_id),
            "timestamp": scan.scan_time.isoformat() if scan.scan_time else None,
            "score": score.score if score else 0
        },
        "rule_results": [] # We don't parse rules deeply in beta yet
    }

# -- Dashboard Policies APIs --
@router.get("/policies")
async def list_policies(db: Session = Depends(get_db), admin: str = Depends(get_current_admin)):
    policies = db.query(Policy).all()
    return [
        {
            "id": str(p.id),
            "name": p.name,
            "os_target": p.os_target,
            "content_id": p.content_id,
            "profile_id": p.profile_id
        }
        for p in policies
    ]

class PolicyCreate(BaseModel):
    name: str
    os_target: str
    content_id: str
    profile_id: str

@router.post("/policies")
async def create_policy(policy: PolicyCreate, db: Session = Depends(get_db), admin: str = Depends(get_current_admin)):
    new_policy = Policy(
        name=policy.name,
        os_target=policy.os_target,
        content_id=policy.content_id,
        profile_id=policy.profile_id
    )
    db.add(new_policy)
    db.commit()
    db.refresh(new_policy)
    return {"id": str(new_policy.id)}

@router.put("/policies/{policy_id}")
async def update_policy(policy_id: int, policy: PolicyCreate, db: Session = Depends(get_db), admin: str = Depends(get_current_admin)):
    db_policy = db.query(Policy).filter(Policy.id == policy_id).first()
    if not db_policy:
        raise HTTPException(status_code=404, detail="Policy not found")
        
    db_policy.name = policy.name
    db_policy.os_target = policy.os_target
    db_policy.content_id = policy.content_id
    db_policy.profile_id = policy.profile_id
    
    db.commit()
    return {"status": "updated"}

@router.delete("/policies/{policy_id}")
async def delete_policy(policy_id: int, db: Session = Depends(get_db), admin: str = Depends(get_current_admin)):
    db_policy = db.query(Policy).filter(Policy.id == policy_id).first()
    if not db_policy:
        raise HTTPException(status_code=404, detail="Policy not found")
        
    db.delete(db_policy)
    db.commit()
    return {"status": "deleted"}
