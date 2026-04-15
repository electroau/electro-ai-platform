from fastapi import FastAPI, UploadFile, File
import pandas as pd

from app.analysis.analyzer import analyze_dataframe

app = FastAPI()

last_analysis = None


@app.get("/")
def root():
    return {"message": "Electro AI Platform Running"}


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    global last_analysis

    # قراءة ملف Excel
    df = pd.read_excel(file.file)

    # تحليل البيانات
    last_analysis = analyze_dataframe(df)

    return {
        "message": "File uploaded and analyzed successfully",
        "columns": last_analysis["columns"]
    }
