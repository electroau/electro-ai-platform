from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Electro AI Platform Running"}
