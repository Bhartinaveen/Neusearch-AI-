import os
from typing import List, Dict

# Use a local persistence directory
CHROMA_DB_DIR = os.path.join(os.path.dirname(__file__), "../chroma_db")

RAG_AVAILABLE = False
try:
    import chromadb
    from chromadb.utils import embedding_functions
    from sentence_transformers import SentenceTransformer
    RAG_AVAILABLE = True
except ImportError:
    print("Warning: RAG dependencies (chromadb/sentence-transformers) not installed. RAG disabled.")

class RAGPipeline:
    def __init__(self):
        self.collection = None
        if RAG_AVAILABLE:
            try:
                self.client = chromadb.PersistentClient(path=CHROMA_DB_DIR)
                # Use sentence-transformers (local)
                self.embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
                self.collection = self.client.get_or_create_collection(
                    name="products",
                    embedding_function=self.embedding_fn
                )
            except Exception as e:
                print(f"Failed to init ChromaDB: {e}")
                self.collection = None

    def add_products(self, products: List[Dict]):
        if not self.collection:
            return
        ids = [str(p['id']) if 'id' in p else p['link'] for p in products]
        documents = []
        metadatas = []

        for p in products:
            # Construct a rich text representation for embedding
            # "Title: X. Price: Y. Description: Z. Features: A, B."
            features_str = ", ".join([f"{k}: {v}" for k, v in p.get('features', {}).items()])
            text = f"Title: {p['title']}. Price: {p['price']}. Category: {p.get('category', '')}. Description: {p.get('description', '')}. Features: {features_str}."
            documents.append(text)
            
            # Metadata for filtering/reference
            meta = {
                "title": p['title'],
                "price": p['price'],
                "link": p.get('link', ''),
                "image_url": p.get('image_url', '')
            }
            metadatas.append(meta)

        self.collection.upsert(
            ids=ids,
            documents=documents,
            metadatas=metadatas
        )
        print(f"Upserted {len(products)} vectors.")

    def query(self, query_text: str, n_results: int = 5):
        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results
        )
        # Unpack results
        items = []
        if results['metadatas']:
            for i, meta in enumerate(results['metadatas'][0]):
                item = meta.copy()
                item['distance'] = results['distances'][0][i] if results['distances'] else 0
                items.append(item)
        return items

rag = RAGPipeline()
