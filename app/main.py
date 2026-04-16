from fastapi import FastAPI, UploadFile, File
import pandas as pd

from app.analysis.analyzer import analyze_dataframe
from app.ai.router import AIRouter
from app.core.context import ContextManager

app = FastAPI()

context = ContextManager()
last_analysis = None


@app.get("/")
def root():
    return {"message": "Electro AI Platform Running"}


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
    global last_analysis

    if last_analysis is None:
        return {"error": "Upload a file first"}

    # ✅ داخل الدالة
    analysis = context.get_data()
    router = AIRouter()
    response = router.route(question, analysis)

    context.add_history(question, response)

    return {"response": response}
