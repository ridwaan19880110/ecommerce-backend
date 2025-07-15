# app/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi_socketio import SocketManager
from dotenv import load_dotenv
from app.api import products
from app.api.products import router as product_router
from app.db.database import engine
from app.db.models import Base
import asyncpg
import os

load_dotenv()

app = FastAPI()

# WebSocket support
socket_manager = SocketManager(app=app)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with allowed frontend origin in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register product router
app.include_router(product_router, prefix="/api")

# Create tables
Base.metadata.create_all(bind=engine)

# Database connection (for legacy support tickets)
DATABASE_URL = os.getenv("SUPABASE_DB_URL")

async def get_db():
    return await asyncpg.connect(DATABASE_URL)

@app.get("/api/support/tickets")
async def list_tickets():
    conn = await get_db()
    rows = await conn.fetch("SELECT * FROM support_tickets ORDER BY submitted_at DESC")
    await conn.close()
    return [dict(row) for row in rows]

@app.put("/api/support/tickets/{ticket_id}")
async def update_ticket_status(ticket_id: int, payload: dict):
    status = payload.get("status")
    if status not in ["open", "closed"]:
        raise HTTPException(status_code=400, detail="Invalid status")
    conn = await get_db()
    await conn.execute("UPDATE support_tickets SET status = $1 WHERE id = $2", status, ticket_id)
    await conn.close()
    return {"status": "updated"}

@socket_manager.on("announcement")
async def handle_announcement(sid, msg):
    await socket_manager.emit("announcement", msg)

@app.get("/")
def read_root():
    return {"message": "API is working 🚀"}

@app.get("/ping")
def ping():
    return {"message": "pong"}