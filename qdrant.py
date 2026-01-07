from typing import List, Optional
from uuid import uuid4

from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from sentence_transformers import SentenceTransformer


class QdrantContentStore:
    """
    Manages content storage in Qdrant with optional semantic chunking.
    """

    def __init__(
        self,
        collection_name: str = "content",
        host: Optional[str] = "localhost",
        port: int = 6333,
        location: Optional[str] = None,
        embedding_model: str = "all-MiniLM-L6-v2",
        vector_size: int = 384,
    ):
        self.collection_name = collection_name
        if location:
            self.client = QdrantClient(location=location)
        else:
            self.client = QdrantClient(host=host, port=port)
        self.model = SentenceTransformer(embedding_model)

        self._ensure_collection(vector_size)

    def _ensure_collection(self, vector_size: int):
        """
        Create Qdrant collection if it does not exist.
        """
        if not self.client.collection_exists(self.collection_name):
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=vector_size,
                    distance=Distance.COSINE,
                ),
            )

    def _semantic_chunk(self, text: str, max_length: int = 400) -> List[str]:
        """
        Simple semantic-friendly chunking (paragraph-based).
        """
        paragraphs = [p.strip() for p in text.split("\n") if p.strip()]
        chunks = []
        current = ""

        for p in paragraphs:
            if len(current) + len(p) <= max_length:
                current += " " + p
            else:
                chunks.append(current.strip())
                current = p

        if current:
            chunks.append(current.strip())

        return chunks

    def add(
        self,
        heading: str,
        text: str,
        image: Optional[str] = None,
        semantic_chunking: bool = False,
    ):
        """
        Add content to Qdrant.
        """
        chunks = (
            self._semantic_chunk(text)
            if semantic_chunking
            else [text]
        )

        points = []

        for chunk in chunks:
            vector = self.model.encode(chunk).tolist()

            payload = {
                "heading": heading,
                "image": image,
                "text": chunk,
            }

            points.append(
                PointStruct(
                    id=str(uuid4()),
                    vector=vector,
                    payload=payload,
                )
            )

        self.client.upsert(
            collection_name=self.collection_name,
            points=points,
        )

    def search(self, query: str, limit: int = 5):
        """
        Semantic search in Qdrant.
        """
        vector = self.model.encode(query).tolist()

        results = self.client.query_points(
            collection_name=self.collection_name,
            query=vector,
            limit=limit,
        ).points

        return [
            {
                "score": r.score,
                "heading": r.payload.get("heading"),
                "image": r.payload.get("image"),
                "text": r.payload.get("text"),
            }
            for r in results
        ]
