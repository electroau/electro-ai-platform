from app.core.context import ContextManager

context = ContextManager()
from fastapi import FastAPI, UploadFile, File
import pandas as pd

from app.analysis.analyzer import analyze_dataframe
from app.ai.engine import ask_ai
from app.core.context import ContextManager
context = ContextManager()

app = FastAPI()

last_analysis = None


@app.get("/")
def root():
    return {"message": "Electro AI Platform Running"}


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    global last_analysis

    df = pd.read_excel(file.file)
    last_analysis = analyze_dataframe(df)
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

    analysis = context.get_data()
response = ask_ai(question, analysis)

context.add_history(question, response)

    return {"response": response}
