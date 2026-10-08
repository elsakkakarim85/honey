from sqlalchemy import Column, Integer, String, Float, Boolean, Date, ForeignKey, Text
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Apiary(Base):
    __tablename__ = "apiaries"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    location_lat = Column(Float)
    location_lon = Column(Float)
    hives = relationship("Hive", back_populates="apiary")

class Hive(Base):
    __tablename__ = "hives"
    id = Column(String, primary_key=True)
    apiary_id = Column(String, ForeignKey("apiaries.id"))
    name_or_number = Column(String)
    hive_type = Column(String) # Langstroth, Top Bar, Warre
    date_established = Column(Date)
    color = Column(String)
    apiary = relationship("Apiary", back_populates="hives")
    inspections = relationship("Inspection", back_populates="hive")
    harvests = relationship("Harvest", back_populates="hive")

class Queen(Base):
    __tablename__ = "queens"
    id = Column(String, primary_key=True)
    hive_id = Column(String, ForeignKey("hives.id"))
    hatch_date = Column(Date)
    breed = Column(String) # Carniolan, Italian, Buckfast
    color_code = Column(String) # Standard international year color
    marked = Column(Boolean, default=False)
    clipped = Column(Boolean, default=False)

class Inspection(Base):
    __tablename__ = "inspections"
    id = Column(String, primary_key=True)
    hive_id = Column(String, ForeignKey("hives.id"))
    date = Column(Date)
    
    # ApiNote core metrics
    temperament = Column(Integer) # 1 (Aggressive) to 5 (Calm)
    population_size = Column(Integer) # 1 to 5
    brood_pattern = Column(Integer) # 1 (Spotty) to 5 (Solid)
    
    # Frames
    frames_of_bees = Column(Float)
    frames_of_brood = Column(Float)
    frames_of_honey = Column(Float)
    
    # Queen status
    queen_seen = Column(Boolean, default=False)
    eggs_seen = Column(Boolean, default=False)
    queen_cells = Column(Boolean, default=False)
    
    # Health
    varroa_count = Column(Integer)
    disease_suspected = Column(String) # AFB, EFB, Chalkbrood, None
    treatment_applied = Column(String)
    
    notes = Column(Text)
    hive = relationship("Hive", back_populates="inspections")

class Harvest(Base):
    __tablename__ = "harvests"
    id = Column(String, primary_key=True)
    hive_id = Column(String, ForeignKey("hives.id"))
    date = Column(Date)
    product_type = Column(String) # Honey, Wax, Pollen, Propolis, Royal Jelly
    weight_kg = Column(Float)
    batch_lot = Column(String)
    hive = relationship("Hive", back_populates="harvests")

class Task(Base):
    __tablename__ = "tasks"
    id = Column(String, primary_key=True)
    apiary_id = Column(String, ForeignKey("apiaries.id"))
    description = Column(String)
    due_date = Column(Date)
    completed = Column(Boolean, default=False)
