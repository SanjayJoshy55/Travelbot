from app.services.rag_service import RagService
import sys

def test_retrieval(query):
    print(f"\nQuery: '{query}'")
    rag = RagService(persist_path="./chroma_db")
    results = rag.query(query, n_results=2)
    
    for i, res in enumerate(results):
        print(f"  Result {i+1}: {res['text']} (Dist: {res['distance']:.4f})")
        print(f"    Meta: {res['metadata']}")

if __name__ == "__main__":
    queries = [
        "What museums are in Paris?",
        "How is the weather in Tokyo?",
        "Tell me about landmarks in New York"
    ]
    
    for q in queries:
        test_retrieval(q)
