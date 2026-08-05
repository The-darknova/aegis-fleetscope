from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Aegis FleetScope API",
    description="Centralized Linux configuration assessment and compliance platform API.",
    version="1.0.0",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json"
)

# CORS middleware for React Dashboard
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Should be restricted in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.api.endpoints import agent, auth, dashboard, scap


@app.get("/api/v1/health", tags=["System"])
async def health_check():
    return {"status": "ok", "service": "Aegis FleetScope Backend"}

# Include routers
app.include_router(agent.router, prefix="/api/v1/agents", tags=["Agents"])
app.include_router(scap.router, prefix="/api/v1/scap", tags=["SCAP Content"])
app.include_router(dashboard.router, prefix="/api/v1/dashboard", tags=["Dashboard"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
