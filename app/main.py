import pandas as pd
import numpy as np
from fastapi import FastAPI, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from .qdrant import QdrantStore


app = FastAPI()
store = QdrantStore("documents", use_semantic_chunking=True)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def read_root():
    return FileResponse("static/index.html")


@app.post("/upload-excel")
def upload_excel(file: UploadFile):
    df = pd.read_excel(file.file)
    df = df.replace([np.nan, np.inf, -np.inf], None)

    records = []
    for _, row in df.iterrows():
        store.add_record(
        heading=row["heading"],
        text=row["text"],
        image=row.get("image")
        )
        records.append(row.to_dict())

    return {"status": "success", "records": records}


@app.get("/data")
def get_data():
    points = store.get_all()
    return [p.payload for p in points]


@app.get("/query")
def query_data(q: str):
    results = store.search(q)
    return [
        {
            "score": result.score,
            "payload": result.payload
        }
        for result in results
    ]