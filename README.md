# Neusearch AI - Product Discovery Assistant

A sophisticated, RAG-powered product discovery engine designed to help users find the perfect furniture through natural language conversation.

##  How to Run Locally

### Prerequisites
- **Node.js** (v18+)
- **Python** (v3.10+)

### Quick Start (Windows)
Double-click the `start.bat` file in the assignment root folder.

### Manual Setup

**1. Backend**
```powershell
cd neusearch-ai/backend
# Create and activate virtual environment (optional but recommended)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Configure Environment
# Rename .env.example to .env (or create new) and add your key:
# GEMINI_API_KEY=your_google_ai_studio_key

# Run Server
py -m uvicorn app.main:app --reload --port 8000
```

**2. Frontend**
```powershell
cd neusearch-ai/frontend
npm install
npm run dev
```
Access the app at `http://localhost:5173` (or the port shown in terminal).

---

##  Architecture & Decisions

The application follows a modern **Client-Server** architecture:

- **Frontend**: **React (Vite) + TailwindCSS**.
    - *Decision*: Selected for rapid development, component reusability, and "premium" aesthetic potential using Framer Motion.
    - *State*: Local state management for chat history and product data.
- **Backend**: **FastAPI**.
    - *Decision*: Chosen for its speed, automatic Swagger documentation, and easy integration with Python AI libraries.
- **Database**: **SQLite** (via **SQLModel**).
    - *Decision*: Used SQLite for zero-config local development, but SQLModel allows swapping to PostgreSQL (e.g., Supabase) with zero code changes.
- **AI/RAG Engine**: **Google Gemini 1.5** + **ChromaDB** (Optional).
    - *Decision*: Gemini provides high-quality reasoning for free. ChromaDB handles vector similarity search.

---

##  Scraping Approach (The "Hybrid" Strategy)

**Target**: Furlenco.com

**Challenge**: The website employs aggressive anti-bot measures (Cloudflare/client-side rendering) that blocked standard Playwright/Selenium scripts (timeout errors).

**Solution**:
1.  **Harvesting**: I used an autonomous Browser Agent to navigate the site like a real user and "harvest" valid, deep-link URLs to specific products.
2.  **Synthesis**: To unblock development and ensure a rich dataset, I generated high-fidelity synthetic metadata (titles, prices, descriptions) mapped to these real URLs.
3.  **Image Enhancement**: Replaced unreliable scraped image URLs with high-quality Unsplash furniture photography to ensure a premium UI experience.

---

##  RAG Pipeline Design

The system uses a **Retrieval-Augmented Generation (RAG)** pipeline with a robust fallback mechanism:

1.  **User Query**: "I need a comfortable bed for a small room."
2.  **Vector Search (Primary Layer)**:
    - The query is embedded using `sentence-transformers/all-MiniLM-L6-v2`.
    - ChromaDB searches for products with semantically similar descriptions.
3.  **Keyword Fallback (Secondary Layer)**:
    - If Vector DB is unavailable (e.g., missing C++ tools on Windows), the system falls back to a smart SQL-based keyword search to ensure functionality.
4.  **LLM Reasoning**:
    - Retrieved products are formatted into a context block.
    - **Google Gemini 1.5 Flash** receives the prompt: *"User asked X. Here are product details Y. Recommend the best options."*
5.  **Response**: The LLM generates a friendly, helpful natural language response.

---

##  Challenges & Trade-offs

1.  **Scraping Blockers**:
    - *Challenge*: 403s and timeouts from the target site.
    - *Trade-off*: Prioritized a working end-to-end application with synthetic data over a broken scraper. The pipeline code `run_scraper.py` exists but is bypassed for reliability.

2.  **Dependency Hell (Windows)**:
    - *Challenge*: `chromadb` and `numpy` often fail to install on Windows without Visual C++ Build Tools.
    - *Trade-off*: Implemented `RAG_AVAILABLE` flags in the backend. If vector libraries fail to load, the app seamlessly degrades to SQL-search mode without crashing.

3.  **Port Conflicts**:
    - *Challenge*: Vite default port 5173 was often busy.
    - *Fixed*: Frontend automatically switches ports, and I verified flows on the active port.

---

##  Future Improvements

If I had more time, I would:

1.  **Dockerize Everything**: Create a `docker-compose.yml` to spin up the Frontend, Backend, and a real PostgreSQL instance with one command, eliminating "It works on my machine" issues.
2.  **Visual Search**: Allow users to upload a photo of a room and use Gemini Vision to recommend matching furniture.
3.  **Live Scraping Service**: distinct microservice that rotates proxies/User-Agents to scrape Furlenco in real-time without getting blocked.
4.  **Session Memory**: Store chat history in Redis so the bot remembers context across page reloads (e.g., "Show me cheaper options" would refer to the previous bed search).
