import pandas as pd
import numpy as np
from fastapi import FastAPI, UploadFile
from qdrant import QdrantStore


app = FastAPI()
store = QdrantStore("documents", use_semantic_chunking=True)


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