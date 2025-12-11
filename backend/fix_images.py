from sqlmodel import Session, select, create_engine
from app.models import Product
import random

# Database connection
sqlite_url = "sqlite:///./neusearch.db"
engine = create_engine(sqlite_url)

# Unsplash Furniture Images (Reliable & High Quality)
IMAGES = {
    "default": [
        "https://images.unsplash.com/photo-1555041469-a586c61ea9bc?auto=format&fit=crop&w=800&q=80", # Sofa
        "https://images.unsplash.com/photo-1505693314120-0d443867891c?auto=format&fit=crop&w=800&q=80", # Bed
        "https://images.unsplash.com/photo-1577140917170-285929fb55b7?auto=format&fit=crop&w=800&q=80", # Table
        "https://images.unsplash.com/photo-1592078615290-033ee584e267?auto=format&fit=crop&w=800&q=80", # Chair
        "https://images.unsplash.com/photo-1524758631624-e2822e304c36?auto=format&fit=crop&w=800&q=80", # Modern Chair
        "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?auto=format&fit=crop&w=800&q=80", # Minimalist
        "https://images.unsplash.com/photo-1616486338812-3dadae4b4ace?auto=format&fit=crop&w=800&q=80", # Living Room
        "https://images.unsplash.com/photo-1556228453-efd6c1ff04f6?auto=format&fit=crop&w=800&q=80", # Couch
    ]
}

def fix_images():
    with Session(engine) as session:
        products = session.exec(select(Product)).all()
        print(f"Updating {len(products)} products...")
        
        for p in products:
            # Pick a random nice image
            new_img = random.choice(IMAGES["default"])
            p.image_url = new_img
            session.add(p)
            
        session.commit()
        print("Successfully updated all product images to Unsplash URLs!")

if __name__ == "__main__":
    fix_images()
