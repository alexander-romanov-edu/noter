from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.routers import auth, exercises, sessions, sets, stats

app = FastAPI(title="Gym Tracker API")

# allow frontend calls
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API routes
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(exercises.router, prefix="/exercises", tags=["exercises"])
app.include_router(sessions.router, prefix="/sessions", tags=["sessions"])
app.include_router(sets.router, prefix="/sets", tags=["sets"])
app.include_router(stats.router, prefix="/stats", tags=["stats"])

# serve frontend
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/")
def frontend():
    return FileResponse("app/static/index.html")
