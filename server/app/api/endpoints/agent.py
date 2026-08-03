import uuid

from fastapi import APIRouter

from app.schemas.agent import (
    AgentRegistration,
    AgentRegistrationResponse,
    AgentTask,
    AgentTasksResponse,
)

router = APIRouter()

# Stub database mapping agent_id to os metadata dict
mock_agent_os_db: dict[str, dict[str, str]] = {}

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
async def register_agent(agent: AgentRegistration):
    agent_id = str(uuid.uuid4())
    mock_agent_os_db[agent_id] = {
        "os_name": agent.os_name,
        "os_version": agent.os_version
    }
    return AgentRegistrationResponse(
        id=agent_id,
        token="mock-jwt-token"
    )

@router.get("/{agent_id}/tasks", response_model=AgentTasksResponse)
async def get_agent_tasks(agent_id: str):
    if agent_id not in mock_agent_os_db:
        # Default for testing purposes if agent is not explicitly registered in our mock DB
        os_name = "ubuntu"
        os_version = "22.04"
    else:
        os_name = mock_agent_os_db[agent_id]["os_name"]
        os_version = mock_agent_os_db[agent_id]["os_version"]
    
    content_id = resolve_scap_content(os_name, os_version)
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
