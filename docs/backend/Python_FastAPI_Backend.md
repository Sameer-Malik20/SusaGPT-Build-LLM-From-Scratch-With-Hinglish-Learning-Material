# 🐍 Python Backend — FastAPI Complete Guide
> **Level:** Beginner → Intermediate | **Language:** Hinglish | **Goal:** Master FastAPI for backend development

---

## 🧭 Core Concepts (Concept-First)

- FastAPI Basics: Routes, parameters
- Database: SQLAlchemy integration
- Authentication: JWT
- Deployment: Docker

---

## 1. 🚀 FastAPI Basics

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# Data model
class Item(BaseModel):
    name: str
    price: float
    description: Optional[str] = None

# GET request
@app.get("/")
async def root():
    return {"message": "Hello World"}

# GET with path parameter
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

# POST request
@app.post("/items/")
async def create_item(item: Item):
    return {"item": item, "status": "created"}
```

---

## 2. 🗄️ Database Integration

```python
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel

# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Model
class ItemModel(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    price = Column(Float)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Database endpoint
@app.get("/db/items")
async def get_items(db: Session = Depends(get_db)):
    items = db.query(ItemModel).all()
    return items
```

---

## 3. 🔐 Authentication (JWT)

```python
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
import jwt

SECRET_KEY = "secret"
ALGORITHM = "HS256"

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Verify user
    user = verify_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
```

---

## 4. 🐳 Docker Deployment

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## ✅ Checklist

- [ ] FastAPI endpoints create kar sakte ho
- [ ] Database integrate kar sakte ho
- [ ] JWT auth implement kar sakte ho
- [ ] Docker me deploy kar sakte ho