from fastapi import APIRouter, HTTPException
from typing import Dict
import uuid

from app.schemas.agent import (
    AgentRegistration, 
    AgentRegistrationResponse, 
    AgentTasksResponse, 
    AgentTask
)

router = APIRouter()

# Stub database mapping agent_id to os_name
mock_agent_os_db: Dict[str, str] = {}

@router.post("/register", response_model=AgentRegistrationResponse, status_code=201)
async def register_agent(agent: AgentRegistration):
    agent_id = str(uuid.uuid4())
    mock_agent_os_db[agent_id] = agent.os_name.lower()
    return AgentRegistrationResponse(
        id=agent_id,
        token="mock-jwt-token"
    )

@router.get("/{agent_id}/tasks", response_model=AgentTasksResponse)
async def get_agent_tasks(agent_id: str):
    if agent_id not in mock_agent_os_db:
        # Default to ubuntu if not found for testing purposes
        os_name = "ubuntu"
    else:
        os_name = mock_agent_os_db[agent_id]
    
    # OS-based content logic stub
    if "ubuntu" in os_name:
        content_id = "ssg-ubuntu2204-ds.xml"
        profile_id = "xccdf_org.ssgproject.content_profile_standard"
    elif "rhel" in os_name or "redhat" in os_name or "centos" in os_name:
        content_id = "ssg-rhel9-ds.xml"
        profile_id = "xccdf_org.ssgproject.content_profile_standard"
    elif "debian" in os_name:
        content_id = "ssg-debian11-ds.xml"
        profile_id = "xccdf_org.ssgproject.content_profile_standard"
    else:
        content_id = "ssg-generic-ds.xml"
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
