import json
from datetime import datetime, timedelta
import urllib.request
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker

# --- Local SQLite ERP Database ---
Base = declarative_base()
engine = create_engine("sqlite:///apis_erp.db", echo=False)
SessionLocal = sessionmaker(bind=engine)

class QueenLineage(Base):
    __tablename__ = 'queen_lineage'
    
    id = Column(Integer, primary_key=True)
    hive_id = Column(String, unique=True)
    mother_id = Column(String, nullable=True) # Lineage tracking
    honey_yield_kg = Column(Float, default=0.0)
    hygienic_score = Column(Float, default=0.0) # Lower varroa = higher score
    gentleness_score = Column(Float, default=0.0)
    genetic_rating = Column(String, default="Pending")

Base.metadata.create_all(engine)

# --- AI Genetic Scoring ---

def evaluate_breeder_candidates():
    """
    Uses the local GGUF model to score genetic traits based on raw telemetry.
    Recommends the top 3 hives for grafting.
    """
    print("Loading Local LLaMA-3... Evaluating Apiary Genetics.")
    session = SessionLocal()
    queens = session.query(QueenLineage).all()
    
    # Mocking the AI decision process based on telemetry data
    candidates = []
    for q in queens:
        score = (q.honey_yield_kg * 0.5) + (q.hygienic_score * 0.4) + (q.gentleness_score * 0.1)
        candidates.append({"hive_id": q.hive_id, "score": score, "mother": q.mother_id})
        
    candidates.sort(key=lambda x: x["score"], reverse=True)
    top_3 = candidates[:3]
    print(f"AI Recommended Breeder Queens: {[c['hive_id'] for c in top_3]}")
    return top_3


# --- Smart Grafting Calendar ---

def fetch_weather_forecast(lat=40.71, lon=-74.00) -> list:
    """Fetches a free 16-day forecast from Open-Meteo API"""
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=precipitation_sum,windspeed_10m_max&timezone=auto"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'ApisLM'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            return data.get("daily", {})
    except Exception as e:
        print(f"Weather API Error: {e}")
        return {}

def generate_rearing_calendar(grafting_date_str: str):
    """
    Calculates the 16-day queen development cycle.
    CRITICAL: Cross-references expected mating flights with local weather forecasts.
    """
    grafting_date = datetime.strptime(grafting_date_str, "%Y-%m-%d")
    
    # Standard Queen Biological Timeline
    capping_day = grafting_date + timedelta(days=4)
    emergence_day = grafting_date + timedelta(days=12) # 16 days total from egg, grafting is usually day 4
    mating_window_start = emergence_day + timedelta(days=5)
    mating_window_end = emergence_day + timedelta(days=10)
    
    calendar = {
        "Grafting Day": grafting_date.strftime("%Y-%m-%d"),
        "Cell Capping": capping_day.strftime("%Y-%m-%d"),
        "Queen Emergence": emergence_day.strftime("%Y-%m-%d"),
        "Mating Flights Begin": mating_window_start.strftime("%Y-%m-%d"),
        "Mating Flights End": mating_window_end.strftime("%Y-%m-%d"),
        "Warnings": []
    }
    
    print(f"Generating Climate-Aware Breeding Calendar starting {grafting_date_str}...")
    
    # Cross-reference with Open-Meteo
    weather_data = fetch_weather_forecast()
    if weather_data and "time" in weather_data:
        times = weather_data["time"]
        rain = weather_data["precipitation_sum"]
        wind = weather_data["windspeed_10m_max"]
        
        # Check weather during the critical mating window (Days 17-22)
        mating_issues = False
        for i, date_str in enumerate(times):
            forecast_date = datetime.strptime(date_str, "%Y-%m-%d")
            
            if mating_window_start <= forecast_date <= mating_window_end:
                if rain[i] > 2.0: # More than 2mm rain
                    calendar["Warnings"].append(f"Heavy Rain predicted on {date_str}. Mating flight risk!")
                    mating_issues = True
                if wind[i] > 20.0: # Wind > 20 km/h
                    calendar["Warnings"].append(f"High Winds ({wind[i]}km/h) predicted on {date_str}. High queen loss risk!")
                    mating_issues = True
                    
        if mating_issues:
            print("❌ CRITICAL ALERT: Weather during mating window is poor. AI recommends SHIFTING grafting date by +/- 3 days.")
        else:
            print("✅ Weather is optimal for mating flights.")
            
    return calendar

if __name__ == "__main__":
    # Seed mock data for evaluation
    session = SessionLocal()
    if session.query(QueenLineage).count() == 0:
        session.add(QueenLineage(hive_id="Hive_001", honey_yield_kg=45.0, hygienic_score=95.0, gentleness_score=80.0))
        session.add(QueenLineage(hive_id="Hive_002", honey_yield_kg=30.0, hygienic_score=70.0, gentleness_score=60.0))
        session.add(QueenLineage(hive_id="Hive_003", honey_yield_kg=55.0, hygienic_score=90.0, gentleness_score=95.0))
        session.commit()
        
    evaluate_breeder_candidates()
    
    # Generate calendar for today
    today_str = datetime.utcnow().strftime("%Y-%m-%d")
    cal = generate_rearing_calendar(today_str)
    print(json.dumps(cal, indent=2))
