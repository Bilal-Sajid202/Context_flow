from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, PointStruct
from sentence_transformers import SentenceTransformer
import uuid


class QdrantStore:
    def __init__(self, collection_name: str, use_semantic_chunking=False):
        self.client = QdrantClient(host="localhost", port=6333)
        self.collection_name = collection_name
        self.use_semantic_chunking = use_semantic_chunking
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        self._create_collection()

    def _create_collection(self):
        if not self.client.collection_exists(self.collection_name):
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=384, distance="Cosine")
            )

    def _chunk_text(self, text: str):
        if not self.use_semantic_chunking:
            return [text]
        sentences = text.split('.')
        return [s.strip() for s in sentences if s.strip()]

    def add_record(self, heading: str, text: str, image=None):
        """
        Add a record with heading, text, and optional image.
        """
        chunks = self._chunk_text(text)
        points = []

        for chunk in chunks:
            vector = self.model.encode(chunk).tolist()
            payload = {
                "heading": heading,
                "text": chunk,
                "image": image
            }

            points.append(
                PointStruct(
                    id=str(uuid.uuid4()),
                    vector=vector,
                    payload=payload  # JSON STORED HERE
                )
            )

        self.client.upsert(self.collection_name, points)

    def get_all(self):
        return self.client.scroll(
            collection_name=self.collection_name,
            limit=100
        )[0]
