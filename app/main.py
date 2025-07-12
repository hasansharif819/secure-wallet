from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.database.db import Base, engine
from app.routes.auth import router as register_router
from app.routes.auth import router as login_router
from app.routes.wallet import router as wallet_router

app = FastAPI()

# Create DB tables on startup
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Enable CORS (adjust allow_origins in production!)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"hello from": "wallet-api"}

# Include routers
app.include_router(register_router)
app.include_router(login_router)
app.include_router(wallet_router)
