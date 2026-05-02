from fastapi import FastAPI
from app.routers import auth, exercises, sessions, sets, stats

app = FastAPI(title="Gym Tracker API")

app.include_router(auth.router)
app.include_router(exercises.router)
app.include_router(sessions.router)
app.include_router(sets.router)
app.include_router(stats.router)


@app.get("/")
def root():
    return {"message": "Gym Tracker API is running"}
