from typing import Optional, Dict
from sqlmodel import SQLModel, Field, Column, JSON

class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    price: str
    description: Optional[str] = None
    features: Dict = Field(default={}, sa_column=Column(JSON))
    image_url: Optional[str] = None
    category: Optional[str] = None
    link: Optional[str] = None
