import requests
import json
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker

# --- Local SQLite ERP Database ---
Base = declarative_base()
engine = create_engine("sqlite:///apis_erp.db", echo=False)
SessionLocal = sessionmaker(bind=engine)

class ClosedDeal(Base):
    __tablename__ = 'closed_deals'
    
    id = Column(Integer, primary_key=True)
    client_name = Column(String)
    address = Column(String)
    lat = Column(Float)
    lon = Column(Float)
    honey_kg_ordered = Column(Float)
    status = Column(String, default="Pending Delivery")

Base.metadata.create_all(engine)

# --- Supply Chain Routing (TSP via OSRM) ---

def calculate_optimal_delivery_route():
    """
    Reads pending deliveries from the local ERP and uses the free OSRM Trip API
    to solve the Traveling Salesperson Problem (TSP) for fuel-efficient routing.
    """
    session = SessionLocal()
    pending = session.query(ClosedDeal).filter_by(status="Pending Delivery").all()
    
    if not pending:
        print("No pending deliveries today.")
        return None
        
    # Factory Coordinates (Start & End point)
    factory_lat, factory_lon = 40.7128, -74.0060
    
    # Format coordinates for OSRM: {longitude},{latitude}
    coords_list = [f"{factory_lon},{factory_lat}"]
    client_mapping = {0: "Factory"}
    
    for idx, deal in enumerate(pending, start=1):
        coords_list.append(f"{deal.lon},{deal.lat}")
        client_mapping[idx] = deal.client_name
        
    coords_str = ";".join(coords_list)
    
    # OSRM Trip API (solves TSP automatically)
    osrm_url = f"https://router.project-osrm.org/trip/v1/driving/{coords_str}?roundtrip=true&source=first&overview=simplified"
    
    print(f"Calculating optimal route for {len(pending)} deliveries...")
    
    try:
        response = requests.get(osrm_url)
        data = response.json()
        
        if data.get("code") == "Ok":
            trip = data["trips"][0]
            waypoints = data["waypoints"]
            
            # Sort waypoints by the optimal trip order
            waypoints.sort(key=lambda x: x["waypoint_index"])
            
            print("\n=== Optimal Delivery Route (TSP Solved) ===")
            print(f"Total Distance: {trip['distance'] / 1000:.2f} km")
            print(f"Estimated Time: {trip['duration'] / 60:.2f} minutes")
            print("Route Order:")
            
            ordered_route = []
            for wp in waypoints:
                client = client_mapping.get(wp["trips_index"], "Unknown")
                ordered_route.append(client)
                print(f" -> {client}")
                
            return {
                "distance_km": round(trip['distance'] / 1000, 2),
                "duration_min": round(trip['duration'] / 60, 2),
                "route": ordered_route,
                "geometry": trip["geometry"]
            }
        else:
            print(f"OSRM Error: {data}")
    except Exception as e:
        print(f"Routing calculation failed: {e}")
        return None

if __name__ == "__main__":
    # Seed mock data
    session = SessionLocal()
    if session.query(ClosedDeal).count() == 0:
        session.add(ClosedDeal(client_name="Aura Botanicals", lat=40.7282, lon=-73.9942, honey_kg_ordered=50.0))
        session.add(ClosedDeal(client_name="Lush Cosmetics", lat=40.7484, lon=-73.9857, honey_kg_ordered=120.0))
        session.add(ClosedDeal(client_name="Whole Foods Market", lat=40.7306, lon=-73.9921, honey_kg_ordered=300.0))
        session.commit()
        
    calculate_optimal_delivery_route()
