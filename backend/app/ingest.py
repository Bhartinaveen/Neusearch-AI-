import json
import sys
import os

# Add current directory to path so we can import app
sys.path.append(os.getcwd())

from sqlmodel import Session, select
from app.database import engine, create_db_and_tables
from app.models import Product
from app.rag import rag


def ingest():
    print("Initializing Database...")
    create_db_and_tables()
    
    json_path = '../scraper/products.json'
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
                # remove 'id' if present in json to let DB assign it
                if 'id' in item:
                    del item['id']
                
                # Ensure features is a dict
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


if __name__ == "__main__":
    ingest()
