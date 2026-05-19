from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import angle_generation, debate, report, history

app = FastAPI(title="DebateForge API")

app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173","http://localhost:5174"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

app.include_router(angle_generation.router, prefix="/api/angle")
app.include_router(debate.router, prefix="/api/debate")
app.include_router(report.router, prefix="/api/report")
app.include_router(history.router, prefix="/api/history")

@app.get("/")
async def root():
    return {"message": "DebateForge API", "status": "running"}
