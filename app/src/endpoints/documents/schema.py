from pydantic import BaseModel
from typing import List, Optional, Any

class DocumentRecord(BaseModel):
    heading: str
    text: str
    image: Optional[str] = None

class SearchResultPayload(BaseModel):
    heading: str
    text: str
    image: Optional[str] = None

class SearchResult(BaseModel):
    score: float
    payload: SearchResultPayload

class UploadResponse(BaseModel):
    status: str
    records: List[Any]
