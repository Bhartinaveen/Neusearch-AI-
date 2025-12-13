from sqlmodel import create_engine, SQLModel, Session
import os
from dotenv import load_dotenv

load_dotenv()


# Default to SQLite for local dev if DATABASE_URL not set
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./neusearch.db")

connect_args = {"check_same_thread": False} if "sqlite" in DATABASE_URL else {}

# Force IPv4 for Postgres to avoid "Network is unreachable" on Render/Supabase
if "postgresql" in DATABASE_URL:
    import socket
    from urllib.parse import urlparse, urlunparse

    try:
        parsed = urlparse(DATABASE_URL)
        if parsed.hostname:
            # Resolve hostname to IPv4 address
            ipv4_address = socket.gethostbyname(parsed.hostname)
            # Replace hostname with IPv4 address in the URL
            DATABASE_URL = parsed._replace(netloc=parsed.netloc.replace(parsed.hostname, ipv4_address)).geturl()
            print(f"Resolved Database Host {parsed.hostname} to IPv4: {ipv4_address}")
    except Exception as e:
        print(f"Warning: Could not resolve database hostname to IPv4: {e}")

engine = create_engine(DATABASE_URL, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
