from pydantic import BaseModel
from typing import List, Optional, Any

class DocumentRecord(BaseModel):
    heading: str
    text: str
    image: Optional[str] = None

class UploadResponse(BaseModel):
    status: str
    records: List[Any]
