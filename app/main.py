from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile, File
import pandas as pd

from app.analysis.analyzer import analyze_dataframe
from app.ai.router import AIRouter
from app.core.context import ContextManager
from app.core.actions import ActionExecutor
from app.core.database import Database

db = Database()
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
context = ContextManager()
last_analysis = None


@app.get("/")
def root():
    return {"message": "Electro AI Platform Running"}
    
@app.get("/work-orders")
def get_work_orders():
    return db.get_work_orders()

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    global last_analysis

    df = pd.read_excel(file.file)
    last_analysis = analyze_dataframe(df)

    # ✅ داخل الدالة
    context.set_data(last_analysis)

    return {
        "message": "File uploaded and analyzed successfully",
        "columns": last_analysis["columns"]
    }


@app.post("/query")
def query_ai(question: str):

    try:
        analysis = context.get_data() or {}

        response = router.route(question, analysis)

        decision_engine = DecisionEngine()
        decisions = decision_engine.analyze(response)

        action_executor = ActionExecutor()
        actions = action_executor.execute(decisions)

        context.add_history(question, response)

        return {
            "response": response,
            "decisions": decisions,
            "actions": actions
        }

    except Exception as e:
        return {
            "error": str(e),
            "type": str(type(e))
        }
