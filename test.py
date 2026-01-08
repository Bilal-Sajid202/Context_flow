from qdrant import QdrantStore


store = QdrantStore("test_collection", use_semantic_chunking=False)


store.add_record(
heading="Test Heading",
text="This is a test document. It has multiple sentences.",
image=None
)


results = store.get_all()


for r in results:
    print(r.payload)