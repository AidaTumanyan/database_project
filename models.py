from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql://aida:abcd@localhost:5432/database_project', echo=True)

Base = declarative_base()

def get_db():
    db = None
    try:
        db = sessionmaker(bind=engine)()
        yield db
    finally:
        if db is not None:
            db.close()


class Transport(Base):
    __tablename__ = 'transport'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    speed = Column(Integer)
    num_cars = Column(Integer)
    fuel = Column(String)


class Route(Base):
    __tablename__ = 'route'

    id = Column(Integer, primary_key=True)
    number = Column(String)
    passengers = Column(Integer)
    cost = Column(Float)
    num_cars = Column(Integer)

    transport_id = Column(Integer, ForeignKey('transport.id'))
    transport = relationship("Transport", backref="routes")


class Path(Base):
    __tablename__ = 'path'

    id = Column(Integer, primary_key=True)
    start = Column(String)
    end = Column(String)
    stop_numbers = Column(Integer)
    distance = Column(Float)

    route_id = Column(Integer, ForeignKey('route.id'))
    route = relationship("Route", backref="paths")



Base.metadata.create_all(engine)


Session = sessionmaker(bind=engine)
session = Session()

