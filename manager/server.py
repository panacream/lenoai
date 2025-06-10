import os
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), "../.env"))

import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from manager.agent import manager_agent  # Ensure this import points to your main agent instance
import uvicorn
from datetime import datetime

# ---
# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
)
logger = logging.getLogger(__name__)

# ---
# Define a simple message schema
class ChatRequest(BaseModel):
    message: str
    context: dict = None  # Optional, for future extensibility

class ChatResponse(BaseModel):
    reply: str


# ---
# Initialize FastAPI app
app = FastAPI()

# ---
# Mount Stock Agent API router
from manager.sub_agents.stock_agent.api import router as stock_router
app.include_router(stock_router, prefix="/api/stock", tags=["stock"])

# Allow CORS for local frontend dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, restrict this!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---
# Main chat endpoint
# ---
# In-memory task history store
# Each entry: {user, request, response, timestamp, status}
task_history = []

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    logger.debug(f"Received chat request: message={request.message!r}, context={request.context!r}")
    try:
        reply = manager_agent.handle_message(request.message)
        logger.debug(f"Agent reply: {reply!r}")
        # Store in task history
        task_history.append({
            "user": "user_1",  # Replace with real user if available
            "request": request.message,
            "response": reply,
            "timestamp": datetime.utcnow().isoformat(),
            "status": "completed"
        })
        return ChatResponse(reply=reply)
    except Exception as e:
        logger.exception("Error processing chat request")
        # Store error in task history
        task_history.append({
            "user": "user_1",
            "request": request.message,
            "response": f"[ERROR] {str(e)}",
            "timestamp": datetime.utcnow().isoformat(),
            "status": "error"
        })
        return ChatResponse(reply=f"[ERROR] {str(e)}")

# ---
# Task history endpoint
from fastapi.responses import JSONResponse

@app.get("/api/task_history")
async def get_task_history():
    return JSONResponse(content=task_history)

# ---
# Health check endpoint
@app.get("/api/healthz")
def health_check():
    return {"status": "ok"}

# ---
# Optional: run with `python manager/server.py`
if __name__ == "__main__":
    print("[INFO] Starting FastAPI server on http://0.0.0.0:3001 ...")
    logger.info("Starting FastAPI server on http://0.0.0.0:3001 ...")
    try:
        uvicorn.run("manager.server:app", host="0.0.0.0", port=3001, reload=True)
    finally:
        print("[INFO] FastAPI server is running and ready to accept requests at http://localhost:3001")
