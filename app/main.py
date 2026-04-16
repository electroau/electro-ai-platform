from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile, File
import pandas as pd
import logging

from app.analysis.analyzer import analyze_dataframe
from app.ai.router import AIRouter
from app.ai.decision import DecisionEngine
from app.core.context import ContextManager
from app.core.actions import ActionExecutor
from app.core.database import Database

# 🔥 Logging (مهم جدًا)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 🔥 App init
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔥 Core systems
context = ContextManager()
router = AIRouter()
decision_engine = DecisionEngine()
action_executor = ActionExecutor()
db = Database()


# =========================
# Root
# =========================
@app.get("/")
def root():
    return {"message": "Electro AI Platform Running"}


# =========================
# Work Orders
# =========================
@app.get("/work-orders")
def get_work_orders():
    try:
        return db.get_work_orders()
    except Exception as e:
        logger.error(f"DB Error: {e}")
        return {"error": "Database error"}


# =========================
# Upload
# =========================
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        df = pd.read_excel(file.file)
        analysis = analyze_dataframe(df)

        context.set_data(analysis)

        return {
            "message": "File uploaded and analyzed successfully",
            "columns": analysis.get("columns", [])
        }

    except Exception as e:
        logger.error(f"Upload Error: {e}")
        return {"error": "Failed to process file"}


# =========================
# Query (🔥 أهم endpoint)
# =========================
@app.post("/query")
def query_ai(question: str):

    try:
        # 🧠 Context
        analysis = context.get_data() or {}

        # 🧠 AI Routing
        response = router.route(question, analysis)

        # 🧠 Decision Layer
        decisions = decision_engine.analyze(response)

        # ⚙️ Actions Layer
        actions = action_executor.execute(decisions)

        # 🧠 Memory
        context.add_history(question, response)

        return {
            "response": response,
            "decisions": decisions,
            "actions": actions
        }

    except Exception as e:
        logger.error(f"Query Error: {e}")

        return {
            "error": "Internal processing error",
            "details": str(e)
        }
