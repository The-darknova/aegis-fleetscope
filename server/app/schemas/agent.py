
from pydantic import BaseModel


class AgentRegistration(BaseModel):
    hostname: str
    os_name: str
    os_version: str
    architecture: str

class AgentRegistrationResponse(BaseModel):
    id: str
    token: str

class AgentTask(BaseModel):
    task_id: str
    content_id: str
    profile_id: str

class AgentTasksResponse(BaseModel):
    tasks: list[AgentTask]
