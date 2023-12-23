from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import List
from pydantic import BaseModel

# Create your FastAPI app
app = FastAPI()

# Define your SQLAlchemy engine and session
engine = create_engine('postgresql://aida:abcd@localhost:5432/database_project')
SessionLocal = sessionmaker(bind=engine)

# Import your SQLAlchemy models
from models import Transport  # Add other models as needed

# Pydantic models for request and response handling
class TransportCreate(BaseModel):
    name: str
    speed: int
    num_cars: int
    fuel: str

class TransportResponse(BaseModel):
    id: int
    name: str
    speed: int
    num_cars: int
    fuel: str

# CRUD operations for Transport
@app.post("/transports/", response_model=TransportResponse)
def create_transport(transport: TransportCreate, db: Session = Depends(SessionLocal)):
    try:
        db_transport = Transport(**transport.dict())
        db.add(db_transport)
        db.commit()
        db.refresh(db_transport)
        return db_transport
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@app.get("/transports/{transport_id}", response_model=TransportResponse)
def read_transport(transport_id: int, db: Session = Depends(SessionLocal)):
    transport = db.query(Transport).filter(Transport.id == transport_id).first()
    if transport is None:
        raise HTTPException(status_code=404, detail="Transport not found")
    return transport

@app.get("/transports/", response_model=List[TransportResponse])
def list_transports(skip: int = 0, limit: int = 10, db: Session = Depends(SessionLocal)):
    transports = db.query(Transport).offset(skip).limit(limit).all()
    return transports

