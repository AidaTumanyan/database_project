from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import List
from models import Session
from models import Transport, Route, Path
from pydantic import BaseModel


from fastapi import FastAPI

app = FastAPI()




engine = create_engine('postgresql://Aida:abcd@localhost:5432/database_project')
SessionLocal = sessionmaker(bind=engine)

# Pydantic models
class RouteCreate(BaseModel):
    number: str
    passengers: int
    cost: float
    num_cars: int
    transport_id: int

class RouteResponse(BaseModel):
    id: int
    number: str
    passengers: int
    cost: float
    num_cars: int
    transport_id: int

class PathCreate(BaseModel):
    start: str
    end: str
    stop_numbers: int
    distance: float
    route_id: int

class PathResponse(BaseModel):
    id: int
    start: str
    end: str
    stop_numbers: int
    distance: float
    route_id: int
# Define the route for /Transport
@app.get("/Transport")
def get_transport():
    # Logic to retrieve transport data goes here
    return {"message": "This endpoint returns transport data"}

@app.get("/")
def read_root():
    return {"Hello": "World"}


def get_transport_data(db: Session):
    transports = db.query(Transport).all()
    return transports

# Define the route for /Transport
@app.get("/Transport")
def get_transport(db: Session = Depends(Session)):
    transport_data = get_transport_data(db)
    return {"transports": [transport.__dict__ for transport in transport_data]}

# CRUD operations for Route
@app.post("/routes/", response_model=RouteResponse)
def create_route(route: RouteCreate, db: Session = Depends(SessionLocal)):
    try:
        db_route = Route(**route.dict())
        db.add(db_route)
        db.commit()
        db.refresh(db_route)
        return db_route
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@app.get("/routes/{route_id}", response_model=RouteResponse)
def read_route(route_id: int, db: Session = Depends(SessionLocal)):
    route = db.query(Route).filter(Route.id == route_id).first()
    if route is None:
        raise HTTPException(status_code=404, detail="Route not found")
    return route

@app.get("/routes/", response_model=List[RouteResponse])
def list_routes(skip: int = 0, limit: int = 10, db: Session = Depends(SessionLocal)):
    routes = db.query(Route).offset(skip).limit(limit).all()
    return routes

# CRUD operations for Path
@app.post("/paths/", response_model=PathResponse)
def create_path(path: PathCreate, db: Session = Depends(SessionLocal)):
    try:
        db_path = Path(**path.dict())
        db.add(db_path)
        db.commit()
        db.refresh(db_path)
        return db_path
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@app.get("/paths/{path_id}", response_model=PathResponse)
def read_path(path_id: int, db: Session = Depends(SessionLocal)):
    path = db.query(Path).filter(Path.id == path_id).first()
    if path is None:
        raise HTTPException(status_code=404, detail="Path not found")
    return path

@app.get("/paths/", response_model=List[PathResponse])
def list_paths(skip: int = 0, limit: int = 10, db: Session = Depends(SessionLocal)):
    paths = db.query(Path).offset(skip).limit(limit).all()
    return paths

