from qdrant import QdrantContentStore


def run_tests():
    print("🚀 Initializing QdrantContentStore...")
    # Use in-memory storage for testing to avoid connection errors
    store = QdrantContentStore(collection_name="test_content", location=":memory:")

    print("\n✅ Test 1: Insert without semantic chunking")
    store.add(
        heading="Test Heading No Chunking",
        text="This is a short test text for Qdrant.",
        image=None,
        semantic_chunking=False,
    )
    print("✔ Inserted single document")

    print("\n✅ Test 2: Insert WITH semantic chunking")
    long_text = """
    Artificial Intelligence is a broad field of computer science.
    It focuses on building systems that can perform tasks
    that normally require human intelligence.

    These tasks include reasoning, learning, perception,
    and language understanding.

    AI is used in healthcare, finance, robotics, and many other domains.
    """

    store.add(
        heading="Test Heading With Chunking",
        text=long_text,
        image="https://example.com/image.png",
        semantic_chunking=True,
    )
    print("✔ Inserted chunked document")

    print("\n🔍 Test 3: Semantic search")
    results = store.search("What is artificial intelligence?", limit=3)

    print("\nSearch Results:")
    for i, r in enumerate(results, start=1):
        print(f"\nResult {i}")
        print("Score :", round(r["score"], 4))
        print("Heading:", r["heading"])
        print("Image :", r["image"])
        print("Text  :", r["text"][:200], "...")


if __name__ == "__main__":
    run_tests()
