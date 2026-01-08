from fastapi import APIRouter, UploadFile, Depends
from typing import List
from .schema import UploadResponse, SearchResult
from ...functionality.documents import ingestion

router = APIRouter(prefix="", tags=["documents"])

@router.post("/upload-excel", response_model=UploadResponse)
async def upload_excel(file: UploadFile):
    return await ingestion.process_excel_upload(file)

@router.get("/data")
def get_data():
    return ingestion.retrieve_all_documents()

@router.get("/query", response_model=List[SearchResult])
def query_data(q: str):
    return ingestion.search_documents_logic(q)
