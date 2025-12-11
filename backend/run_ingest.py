import json
import sys
import os

# Debug
print(f"CWD: {os.getcwd()}")
print(f"Sys Path before: {sys.path}")
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)
print(f"Sys Path after: {sys.path}")

try:
    from app.database import engine, create_db_and_tables
    from app.models import Product
    from app.rag import rag
except ImportError as e:
    print(f"Import Error: {e}")
    # Try looking in subfolder if failed
    sys.exit(1)

def ingest():
    print("Initializing Database...")
    create_db_and_tables()
    
    json_path = os.path.join(current_dir, '../scraper/products.json')
    if not os.path.exists(json_path):
        print(f"File not found: {json_path}")
        return

    print(f"Reading from {json_path}...")
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"Found {len(data)} products in JSON.")
    
    with Session(engine) as session:
        count = 0
        for item in data:
            # deduplicate by link
            existing = session.exec(select(Product).where(Product.link == item['link'])).first()
            if not existing:
                if 'id' in item:
                    del item['id']
                if 'features' in item and item['features'] is None:
                    item['features'] = {}
                    
                product = Product(**item)
                session.add(product)
                count += 1
        session.commit()
        
        # Add to Vector DB
        if data:
            print("Adding to Vector DB...")
            rag.add_products(data)
            
    print(f"Successfully ingested {count} new products and updated vectors.")
    
from sqlmodel import Session, select # Import here to use in function

if __name__ == "__main__":
    ingest()
