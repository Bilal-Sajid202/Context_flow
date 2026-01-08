import pandas as pd
import numpy as np
from fastapi import UploadFile
from ...DAL.qdrant import QdrantStore
from ...services.validator import validate_excel_file

# Initialize store
store = QdrantStore("documents", use_semantic_chunking=True)

async def process_excel_upload(file: UploadFile):
    # Service validation
    validate_excel_file(file)

    # Functionality logic
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

def retrieve_all_documents():
    points = store.get_all()
    # Safely handle payload (ensure it's not None)
    return [p.payload for p in points if p.payload]

def search_documents_logic(query: str):
    results = store.search(query)
    return [
        {
            "score": result.score,
            "payload": result.payload
        }
        for result in results
    ]
