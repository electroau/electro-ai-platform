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
# Logging (Production-ready)
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
    version="2.0.0"
)


# =========================
# CORS (Production safer)
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # لاحقاً نحدد الدومين
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# Dependency Injection (بدل Global State)
# =========================
def get_context():
    return ContextManager()


def get_router():
    return AIRouter()


def get_decision_engine():
    return DecisionEngine()


def get_action_executor():
    return ActionExecutor()


def get_db():
    return Database()


def get_orchestrator(
    router: AIRouter = Depends(get_router),
    decision_engine: DecisionEngine = Depends(get_decision_engine),
    action_executor: ActionExecutor = Depends(get_action_executor),
):
    return AIOrchestrator(
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
        "system": "Electro AI Platform",
        "version": "2.0"
    }


# =========================
# Health Check
# =========================
@app.get("/health")
def health():
    return {
        "status": "ok"
    }


# =========================
# Work Orders
# =========================
@app.get("/work-orders")
def get_work_orders(db: Database = Depends(get_db)):
    try:
        return db.get_work_orders()
    except Exception:
        logger.exception("DB Error")
        return {"error": "Database error"}


# =========================
# Upload (Data Ingestion)
# =========================
@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    context: ContextManager = Depends(get_context)
):
    try:
        df = pd.read_excel(file.file)
        analysis = analyze_dataframe(df)

        context.set_data(analysis)

        logger.info("File uploaded and analyzed")

        return {
            "message": "File uploaded and analyzed successfully",
            "columns": analysis.get("columns", [])
        }

    except Exception:
        logger.exception("Upload failed")
        return {"error": "Failed to process file"}


# =========================
# Query (🔥 Orchestrator Entry Point)
# =========================
@app.post("/query")
def query_ai(
    request: QueryRequest,
    context: ContextManager = Depends(get_context),
    db: Database = Depends(get_db),
    orchestrator: AIOrchestrator = Depends(get_orchestrator)
):
    try:
        # =========================
        # Build Business Context 🔥
        # =========================
        business_context = {
            "client": db.get_client(request.client_id) if request.client_id else None,
            "equipment": db.get_equipment(request.equipment_id) if request.equipment_id else None,
            "history": db.get_history(request.client_id) if request.client_id else [],
            "analysis": context.get_data() or {}
        }

        # =========================
        # AI Orchestrator
        # =========================
        result = orchestrator.run(request.question, business_context)

        # =========================
        # Memory
        # =========================
        context.add_history(request.question, result.get("response"))

        logger.info(f"Query processed: {request.question}")

        return result

    except Exception as e:
        logger.exception("Query processing failed")

        return {
            "error": "Internal processing error",
            "details": str(e)
        }
