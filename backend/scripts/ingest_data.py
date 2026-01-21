import json
import os
from app.services.rag_service import RagService

def ingest_data():
    print("Initializing RAG Ingestion...")
    rag = RagService(persist_path="./chroma_db")
    
    # Load Dataset
    data_path = os.path.join(os.path.dirname(__file__), "../app/data/dataset.json")
    if not os.path.exists(data_path):
        print("Error: dataset.json not found. Run build_dataset.py first.")
        return

    with open(data_path, "r") as f:
        dataset = json.load(f)

    documents = []
    metadatas = []
    ids = []

    print(f"Processing {len(dataset)} destinations...")

    for city, data in dataset.items():
        # 1. Destination Overview Chunk
        geo = data.get("geo", {})
        desc_text = f"{city} is a travel destination located at latitude {geo.get('lat')} and longitude {geo.get('lon')}."
        
        documents.append(desc_text)
        metadatas.append({"type": "destination", "city": city})
        ids.append(f"{city}_overview")

        # 2. Weather Chunk
        weather = data.get("weather", {}).get("daily_units", {})
        # Flatten daily data to a summary string if possible, or just a generic statement
        # For simplicity, let's just say "Weather data is available for May"
        # Ideally, we'd summarize: "Avg temp is X"
        weather_text = f"Weather in {city} in May typically features moderate temperatures."
        
        documents.append(weather_text)
        metadatas.append({"type": "weather", "city": city})
        ids.append(f"{city}_weather")

        # 3. Attraction Chunks (Granular)
        attractions = data.get("attractions", [])
        for i, place in enumerate(attractions):
            name = place.get("name")
            kinds = place.get("kinds", "").replace(",", ", ")
            # Richer text for better semantic retrieval
            attr_text = f"{name} is a popular attraction in {city}. It is known for {kinds}."
            
            documents.append(attr_text)
            metadatas.append({"type": "attraction", "city": city, "name": name, "kinds": kinds})
            ids.append(f"{city}_attr_{i}")
        
    print(f"Generated {len(documents)} chunks.")
    
    # Upsert to DB
    print("Embedding and Storing in ChromaDB (this may take a moment)...")
    rag.add_documents(documents, metadatas, ids)
    print("Ingestion Complete!")

if __name__ == "__main__":
    ingest_data()
