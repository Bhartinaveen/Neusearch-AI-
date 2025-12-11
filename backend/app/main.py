from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
import os

from sqlmodel import Session, select
from typing import List
from .database import create_db_and_tables, get_session
import app.database as from_database
from .models import Product


from dotenv import load_dotenv
load_dotenv()

app = FastAPI(title="Neusearch AI API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def read_root():
    return {"message": "Welcome to Neusearch AI Backend"}

@app.get("/products", response_model=List[Product])
def get_products(session: Session = Depends(get_session)):
    products = session.exec(select(Product)).all()
    return products

@app.get("/products/{product_id}", response_model=Product)
def get_product(product_id: int, session: Session = Depends(get_session)):
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

from pydantic import BaseModel
from .rag import rag

class ChatRequest(BaseModel):
    query: str

@app.post("/chat")
def chat(request: ChatRequest):
    try:
        results = []
        if rag.collection:
            try:
                results = rag.query(request.query)
            except Exception as e:
                print(f"RAG Query failed: {e}")
        
        # Fallback to Simple SQL Search if RAG is disabled or returns no results
        if not results:
            print("Using SQL Fallback Search")
            # Create a new session for fallback search
            with Session(from_database.engine) as session:
                # Basic keyword splitting
                keywords = request.query.lower().split()
                # Remove common stop words (very basic)
                stop_words = {"i", "want", "need", "looking", "for", "a", "the", "in", "my", "to", "can", "you", "recommend", "show", "me"}
                search_terms = [k for k in keywords if k not in stop_words]
                
                if not search_terms:
                    # Provide *some* results if query is too generic
                    results_obj = session.exec(select(Product).limit(5)).all()
                else:
                    # Build a query that matches ANY valid keyword in title or description
                    # For simplicity in SQLite/Demonstration, we'll do python-side filtering or multiple contains
                    # Ideally use Postgres Full Text Search, but we must support SQLite local too.
                    all_products = session.exec(select(Product)).all()
                    
                    scored_products = []
                    for p in all_products:
                        score = 0
                        text = (p.title + " " + (p.description or "") + " " + str(p.category)).lower()
                        for term in search_terms:
                            if term in text:
                                score += 1
                        if score > 0:
                            scored_products.append((score, p))
                    
                    # Sort by score desc
                    scored_products.sort(key=lambda x: x[0], reverse=True)
                    results_obj = [p for _, p in scored_products[:5]]
                
                # Convert SQL models to dict for response consistency with RAG
                results = [p.model_dump() for p in results_obj]

        # Prepare context for Gemini
        context_text = ""
        if results:
            context_text = "Found Products:\n"
            for p in results:
                # Handle both dict (from SQL) and object (if changed later)
                p_text = f"- {p.get('title', 'Unknown')} (${p.get('price', 'N/A')}): {p.get('description', '')[:200]}..."
                context_text += p_text + "\n"
        else:
            context_text = "No specific products found in the database matching the criteria."

        # Generate Response using Gemini
        try:
            if os.getenv("GEMINI_API_KEY"):
                genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
                model = genai.GenerativeModel('gemma-3-27b-it')
                
                prompt = f"""
                You are a helpful and enthusiastic furniture shopping assistant for 'Neusearch AI'.
                The user asked: "{request.query}"
                
                Here is the product information found in our catalog:
                {context_text}
                
                Please answer the user's question recommending the above products if they are relevant.
                
                Important:
                - If the user asks an abstract question (e.g., "how to furnish a 3BHK", "ideas for a living room"), provide helpful, high-level interior design advice and suggest types of furniture they might need.
                - If specific products were found in the context above and they are relevant to the user's need, specifically recommend them as options to fulfill that advice.
                - If no specific products were found in the context, you can still give general advice about what to look for, but do not invent specific product names or prices that aren't in the catalog.
                
                Keep the response concise, friendly, and encouraging.
                """
                
                generated_response = model.generate_content(prompt)
                response_text = generated_response.text
            else:
                # Fallback if no key
                print("GEMINI_API_KEY not found in environment variables.")
                # Use the basic constructed response from before
                response_text = f"Here are some recommendations for '{request.query}':"
                if not results:
                     response_text = "I couldn't find any specific products matching your detailed request, but here are some of our popular items:"

        except Exception as e:
            print(f"Gemini API Error: {e}")
            # Fallback on error - show error to user so they know why it failed
            response_text = f"I'm sorry, I'm having trouble thinking right now. (Error: {str(e)})"
            if results:
                response_text += " But I found these products for you:"

        return {
            "response": response_text,
            "recommendations": results
        }
    except Exception as e:
        print(f"Chat Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
