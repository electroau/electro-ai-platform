from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from typing import Optional
import shutil
import os

from app.ai.orchestrator import AIOrchestrator
from app.ai.router import AIRouter
from app.ai.decision import DecisionEngine
from app.core.context import ContextManager
from app.core.actions import ActionExecutor
from app.core.database import Database


# =========================
# Init
# =========================
app = FastAPI(title="Electro AI Platform", version="3.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# Core Systems
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
# Models
# =========================
class QueryRequest(BaseModel):
    question: str
    session_id: Optional[str] = None


# =========================
# Upload PDF 🔥
# =========================
@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        os.makedirs("docs", exist_ok=True)

        file_path = os.path.join("docs", file.filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 🔥 إضافة مباشرة للـ RAG
        orchestrator.rag.add_pdf(file_path)

        return {
            "message": "PDF uploaded and indexed",
            "file": file.filename
        }

    except Exception as e:
        return {"error": str(e)}


# =========================
# Query
# =========================
@app.post("/query")
def query_ai(request: QueryRequest):
    try:
        sid = request.session_id or "default"

        ctx = {
            "analysis": context.get_data(sid),
            "history": context.get_history(sid)
        }

        result = orchestrator.run(request.question, ctx)

        context.add_history(
            sid,
            request.question,
            result.get("response")
        )

        return result

    except Exception as e:
        return {"error": str(e)}
