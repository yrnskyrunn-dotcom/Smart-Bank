from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from .routers import auth, users, accounts, transactions

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Smart Bank API", version="0.1.0")

# CORS for local dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(accounts.router)
app.include_router(transactions.router)

@app.get("/")
def root():
    return {"name": "Smart Bank", "status": "ok"}
