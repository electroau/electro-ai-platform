from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile, File, Depends
from pydantic import BaseModel
from typing import Optional
import pandas as pd
import logging

from app.analysis.analyzer import analyze_dataframe
from app.ai.router import AIRouter
from app.ai.decision import DecisionEngine
from app.ai.orchestrator import AIOrchestrator
from app.core.context import ContextManager
from app.core.actions import ActionExecutor
from app.core.database import Database


# =========================
# Logging
# =========================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)
logger = logging.getLogger("electro-ai")


# =========================
# App Init
# =========================
app = FastAPI(
    title="Electro AI Platform",
    version="2.2.0"
)


# =========================
# CORS
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# 🔥 SINGLETONS (مهم جداً)
# =========================
context = ContextManager()
router = AIRouter()
decision_engine = DecisionEngine()
action_executor = ActionExecutor()
db = Database()

orchestrator = AIOrchestrator(
    router=router,
    decision_engine=decision_engine,
    action_executor=action_executor
)


# =========================
# Request Models
# =========================
class QueryRequest(BaseModel):
    question: str
    client_id: Optional[int] = None
    equipment_id: Optional[int] = None
    session_id: Optional[str] = None


# =========================
# Root
# =========================
@app.get("/")
def root():
    return {
        "status": "running",
        "version": "2.2"
    }


@app.get("/health")
def health():
    return {"status": "ok"}


# =========================
# Work Orders
# =========================
@app.get("/work-orders")
def get_work_orders():
    try:
        return db.get_work_orders()
    except Exception:
        logger.exception("DB Error")
        return {"error": "Database error"}


# =========================
# Upload
# =========================
@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    session_id: Optional[str] = None
):
    try:
        sid = session_id or "default"

        df = pd.read_excel(file.file)
        analysis = analyze_dataframe(df)

        context.set_data(sid, analysis)

        return {
            "message": "File processed",
            "session_id": sid
        }

    except Exception:
        logger.exception("Upload failed")
        return {"error": "Upload failed"}


# =========================
# Query
# =========================
@app.post("/query")
def query_ai(request: QueryRequest):
    try:
        sid = request.session_id or "default"

        business_context = {
            "client": db.get_client(request.client_id),
            "equipment": db.get_equipment(request.equipment_id),
            "history": db.get_history(request.client_id),
            "analysis": context.get_data(sid)
        }

        result = orchestrator.run(request.question, business_context)

        context.add_history(
            sid,
            request.question,
            result.get("response")
        )

        return result

    except Exception as e:
        logger.exception("Query failed")
        return {
            "error": "Internal error",
            "details": str(e)
        }
