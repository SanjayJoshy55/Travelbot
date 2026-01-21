import chromadb
from chromadb.utils import embedding_functions
from typing import List, Dict, Any

class RagService:
    """
    Manages the Vector Database (ChromaDB) for RAG.
    """
    def __init__(self, persist_path: str = "./chroma_db"):
        # Initialize Persistent Client
        self.client = chromadb.PersistentClient(path=persist_path)
        
        # Use a standard, small model for embeddings
        # 'all-MiniLM-L6-v2' is great for speed/quality balance
        self.embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
        
        # Get or Create Collection
        self.collection = self.client.get_or_create_collection(
            name="travel_knowledge",
            embedding_function=self.embedding_fn
        )

    def add_documents(self, documents: List[str], metadatas: List[Dict[str, Any]], ids: List[str]):
        """
        Adds text chunks + metadata to the vector store.
        """
        self.collection.upsert(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )

    def query(self, query: str, n_results: int = 3) -> List[Dict]:
        """
        Retrieves top-k relevant documents for a query.
        Returns a list of dicts with 'text' and 'metadata'.
        """
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        # Flatten the structure for easier consumption
        flat_results = []
        if results and results['documents']:
            for i in range(len(results['documents'][0])):
                flat_results.append({
                    "text": results['documents'][0][i],
                    "metadata": results['metadatas'][0][i] if results['metadatas'] else {},
                    "distance": results['distances'][0][i] if results['distances'] else 0.0
                })
        
        return flat_results
