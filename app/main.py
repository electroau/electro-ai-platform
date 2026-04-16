from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile, File
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
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# Core Systems (Singleton Style)
# =========================
context = ContextManager()
router = AIRouter()
decision_engine = DecisionEngine()
action_executor = ActionExecutor()
db = Database()

# 🔥 العقل المركزي
orchestrator = AIOrchestrator(
    router=router,
    decision_engine=decision_engine,
    action_executor=action_executor
)


# =========================
# Root
# =========================
@app.get("/")
def root():
    return {
        "status": "running",
        "system": "Electro AI Platform",
        "version": "1.0"
    }


# =========================
# Health Check (مهم جدًا)
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
def get_work_orders():
    try:
        return db.get_work_orders()
    except Exception as e:
        logger.exception("DB Error")
        return {"error": "Database error"}


# =========================
# Upload (Data Ingestion)
# =========================
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        df = pd.read_excel(file.file)
        analysis = analyze_dataframe(df)

        context.set_data(analysis)

        logger.info("File uploaded and analyzed")

        return {
            "message": "File uploaded and analyzed successfully",
            "columns": analysis.get("columns", [])
        }

    except Exception as e:
        logger.exception("Upload failed")
        return {"error": "Failed to process file"}


# =========================
# Query (🔥 Orchestrator Entry Point)
# =========================
@app.post("/query")
def query_ai(question: str):

    try:
        # 🧠 Context
        analysis = context.get_data() or {}

        # 🔥 AI Orchestrator (العقل المركزي)
        result = orchestrator.run(question, analysis)

        # 🧠 Memory
        context.add_history(question, result.get("response"))

        logger.info(f"Query processed: {question}")

        return result

    except Exception as e:
        logger.exception("Query processing failed")

        return {
            "error": "Internal processing error",
            "details": str(e)
        }
