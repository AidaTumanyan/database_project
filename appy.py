from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import List
from models import Session
from models import Transport, Route, Path,get_db
from pydantic import BaseModel


from fastapi import FastAPI

app = FastAPI()




engine = create_engine('postgresql://Aida:abcd@localhost:5432/database_project')
SessionLocal = sessionmaker(bind=engine)

# Pydantic models
class Route(BaseModel):
    id: int
    number: str
    passengers: int
    cost: float
    num_cars: int
    transport_id: int

class Path(BaseModel):
    id: int
    start: str
    end: str
    stop_numbers: int
    distance: float
    route_id: int

class Transport(BaseModel):
    id: int
    name: str
    speed: int
    num_cars: int
    fuel: str


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
@app.post("/routes/", response_model=Route)
def create_route(route: Route, db: Session = Depends(SessionLocal)):
    try:
        db_route = Route(**route.dict())
        db.add(db_route)
        db.commit()
        db.refresh(db_route)
        return db_route
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@app.get("/routes/{route_id}", response_model=Route)
def read_route(route_id: int, db: Session = Depends(SessionLocal)):
    route = db.query(Route).filter(Route.id == route_id).first()
    if route is None:
        raise HTTPException(status_code=404, detail="Route not found")
    return route

@app.get("/routes/", response_model=List[Route])
def list_routes(skip: int = 0, limit: int = 10, db: Session = Depends(SessionLocal)):
    routes = db.query(Route).offset(skip).limit(limit).all()
    return routes

# CRUD operations for Path
@app.post("/paths/", response_model=Path)
def create_path(path: Path, db: Session = Depends(SessionLocal)):
    try:
        db_path = Path(**path.dict())
        db.add(db_path)
        db.commit()
        db.refresh(db_path)
        return db_path
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@app.get("/paths/{path_id}", response_model=Path)
def read_path(path_id: int, db: Session = Depends(SessionLocal)):
    path = db.query(Path).filter(Path.id == path_id).first()
    if path is None:
        raise HTTPException(status_code=404, detail="Path not found")
    return path

@app.get("/paths/", response_model=List[Path])
def list_paths(skip: int = 0, limit: int = 10, db: Session = Depends(SessionLocal)):
    paths = db.query(Path).offset(skip).limit(limit).all()
    return paths







# 1. SELECT ... WHERE (с несколькими условиями)
@app.get("/routes/filter/", response_model=List[Route])
def filter_routes(transport_id: int, passengers: int, db: Session = Depends(get_db)):
    routes = db.query(Route).filter(
        Route.transport_id == transport_id,
        Route.passengers >= passengers
    ).all()
    return routes

# 2. JOIN
@app.get("/transport/{transport_id}/routes/", response_model=List[Route])
def get_transport_routes(transport_id: int, db: Session = Depends(get_db)):
    transport = db.query(Transport).filter(Transport.id == transport_id).first()
    if not transport:
        raise HTTPException(status_code=404, detail="Transport not found")
    return transport.routes

# 3. UPDATE с нетривиальным условием
@app.put("/update-route-cost/", response_model=Route)
def update_route_cost(route_id: int, new_cost: float, db: Session = Depends(get_db)):
    route = db.query(Route).filter(Route.id == route_id).first()
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    route.cost = new_cost
    db.commit()
    db.refresh(route)
    return route

# 4. GROUP BY
@app.get("/routes-by-transport/", response_model=List[dict])
def routes_by_transport(db: Session = Depends(get_db)):
    result = db.query(Route.transport_id, func.count(Route.id)).group_by(Route.transport_id).all()
    return [{"transport_id": transport_id, "route_count": count} for transport_id, count in result]

# 5. Добавить сортировку выдачи результатов по какому-то из полей
@app.get("/paths/", response_model=List[Path])
def list_paths_sorted(start: str, end: str, db: Session = Depends(get_db)):
    paths = db.query(Path).filter(Path.start == start, Path.end == end).order_by(Path.distance).all()
    return paths
