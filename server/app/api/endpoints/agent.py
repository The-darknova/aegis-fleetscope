import uuid
from datetime import UTC, datetime

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.security import create_access_token, get_current_agent
from app.db.session import get_db
from app.models.compliance import ComplianceScore
from app.models.host import Host
from app.models.policy import Policy
from app.models.scan import HistoricalScan
from app.schemas.agent import (
    AgentRegistration,
    AgentRegistrationResponse,
    AgentTask,
    AgentTasksResponse,
)

router = APIRouter()

def resolve_scap_content(os_name: str, os_version: str) -> str:
    """
    Resolve the correct SCAP Security Guide (SSG) datastream filename 
    based on the OS name and version.
    """
    os_name = os_name.lower().strip()
    os_version = os_version.lower().strip()
    
    if "ubuntu" in os_name:
        # e.g. "22.04" -> "2204"
        parts = os_version.split(".")
        if len(parts) >= 2:
            major_minor = f"{parts[0]}{parts[1]}"
        else:
            major_minor = parts[0]
        return f"ssg-ubuntu{major_minor}-ds.xml"
        
    elif "rhel" in os_name or "redhat" in os_name:
        major = os_version.split(".")[0]
        return f"ssg-rhel{major}-ds.xml"
        
    elif "centos" in os_name:
        major = os_version.split(".")[0]
        return f"ssg-centos{major}-ds.xml"
        
    elif "debian" in os_name:
        major = os_version.split(".")[0]
        return f"ssg-debian{major}-ds.xml"
        
    elif "amazon" in os_name or "amzn" in os_name:
        major = os_version.split(".")[0]
        return f"ssg-amzn{major}-ds.xml"
        
    elif "fedora" in os_name:
        major = os_version.split(".")[0]
        return f"ssg-fedora{major}-ds.xml"
        
    elif "suse" in os_name or "sles" in os_name:
        major = os_version.split(".")[0]
        return f"ssg-sle{major}-ds.xml"
    
    return "ssg-generic-ds.xml"

@router.post("/register", response_model=AgentRegistrationResponse, status_code=201)
async def register_agent(agent: AgentRegistration, db: Session = Depends(get_db)):
    # Check if host exists
    db_host = db.query(Host).filter(Host.hostname == agent.hostname).first()
    
    if not db_host:
        db_host = Host(
            hostname=agent.hostname,
            ip_address="0.0.0.0", # TODO: Get real IP from request if needed
            os_name=agent.os_name,
            os_version=agent.os_version,
            architecture=agent.architecture
        )
        db.add(db_host)
        db.commit()
        db.refresh(db_host)
    else:
        # Update existing host
        db_host.os_name = agent.os_name
        db_host.os_version = agent.os_version
        db_host.architecture = agent.architecture
        db_host.last_seen = datetime.now(UTC)
        db.commit()
        db.refresh(db_host)

    # Issue token
    token = create_access_token(subject=str(db_host.id))
    
    return AgentRegistrationResponse(
        id=str(db_host.id),
        token=token
    )

@router.get("/{agent_id}/tasks", response_model=AgentTasksResponse)
async def get_agent_tasks(agent_id: int, db: Session = Depends(get_db), current_agent: int = Depends(get_current_agent)):
    if current_agent != agent_id:
        raise HTTPException(status_code=403, detail="Not authorized to access tasks for this agent")
        
    db_host = db.query(Host).filter(Host.id == agent_id).first()
    if not db_host:
        raise HTTPException(status_code=404, detail="Agent not found")
        
    db_host.last_seen = datetime.now(UTC)
    db.commit()
    
    content_id = resolve_scap_content(db_host.os_name, db_host.os_version)
    
    # Check if there's a specific policy assigned, otherwise use a default
    # For now, just generate one task based on OS
    profile_id = "xccdf_org.ssgproject.content_profile_standard"
        
    return AgentTasksResponse(
        tasks=[
            AgentTask(
                task_id=str(uuid.uuid4()),
                content_id=content_id,
                profile_id=profile_id
            )
        ]
    )

@router.post("/{agent_id}/reports", status_code=202)
async def upload_report(agent_id: int, report: UploadFile = File(...), db: Session = Depends(get_db), current_agent: int = Depends(get_current_agent)):
    if current_agent != agent_id:
        raise HTTPException(status_code=403, detail="Not authorized to upload reports for this agent")
        
    db_host = db.query(Host).filter(Host.id == agent_id).first()
    if not db_host:
        raise HTTPException(status_code=404, detail="Agent not found")
        
    xml_content = await report.read()
    
    # Simple XML mock parsing for beta, in real life we would parse OVAL/XCCDF XML
    # Assuming the xml contains some rules
    passed = 95
    failed = 5
    total = 100
    score = (passed / total) * 100 if total > 0 else 0
    
    # Get or create a default policy for now
    policy = db.query(Policy).first()
    if not policy:
        policy = Policy(
            name="Default Policy",
            os_target="Generic",
            content_id="ssg-generic-ds.xml",
            profile_id="xccdf_org.ssgproject.content_profile_standard"
        )
        db.add(policy)
        db.commit()
        db.refresh(policy)
        
    scan = HistoricalScan(
        host_id=db_host.id,
        policy_id=policy.id,
        passed_rules=passed,
        failed_rules=failed,
        total_rules=total,
        raw_report_xml=xml_content.decode("utf-8", errors="ignore")
    )
    db.add(scan)
    
    comp_score = ComplianceScore(
        host_id=db_host.id,
        policy_id=policy.id,
        score=score
    )
    db.add(comp_score)
    db.commit()
    
    return {"status": "accepted"}
