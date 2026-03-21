from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.summary import router

app = FastAPI(title="Aura Backend", version="3.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/")
def root():
    return {"message": "Aura Backend Running 🚀"}