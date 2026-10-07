from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import math

app = FastAPI()

class HiveState(BaseModel):
    bee_population: int
    varroa_population: int
    queen_age_months: int
    food_stores_kg: float
    user_action: str

class SimulationResult(BaseModel):
    day: int
    bee_population: int
    varroa_population: int
    food_stores_kg: float
    status: str

# Biological constants
QUEEN_LAYING_RATE_MAX = 2000
WORKER_LIFESPAN_DAYS = 42
VARROA_DOUBLING_TIME_DAYS = 21 # Approx in brood

def simulate_30_days(initial_state: HiveState) -> list[SimulationResult]:
    """
    Core Biological Simulation Logic:
    Models population dynamics, Varroa infestation curves, and treatment efficacy.
    """
    timeline = []
    
    current_bees = initial_state.bee_population
    current_varroa = initial_state.varroa_population
    food = initial_state.food_stores_kg
    
    # Parse User Action impacts
    treatment_efficacy = 0.0
    if "Oxalic Acid" in initial_state.user_action:
        treatment_efficacy = 0.85 # Kills 85% of phoretic mites
    elif "Formic Pro" in initial_state.user_action:
        treatment_efficacy = 0.95 # Kills mites under cappings too
    elif "Feed Sugar" in initial_state.user_action:
        food += 5.0
        
    for day in range(1, 31):
        # 1. Queen Laying (Logistic curve based on food and space)
        lay_rate = QUEEN_LAYING_RATE_MAX * (1 if food > 2 else 0.2)
        new_bees = int(lay_rate * 0.9) # 90% survival to emergence
        
        # 2. Natural bee death (assuming uniform age distribution for simplicity)
        dying_bees = int(current_bees / WORKER_LIFESPAN_DAYS)
        
        # 3. Varroa Exponential Growth
        # Varroa population doubles every ~21 days during brood rearing
        varroa_growth_factor = math.pow(2, 1.0 / VARROA_DOUBLING_TIME_DAYS)
        current_varroa = int(current_varroa * varroa_growth_factor)
        
        # Apply treatment on Day 1
        if day == 1 and treatment_efficacy > 0:
            current_varroa = int(current_varroa * (1.0 - treatment_efficacy))
            
        # 4. Varroa Parasitism Impact on Bees
        # High infestation (>3%) severely reduces bee lifespan (viruses like DWV)
        infestation_rate = current_varroa / max(1, current_bees)
        if infestation_rate > 0.03:
            # Accelerated death rate due to Deformed Wing Virus (DWV) and stress
            viral_collapse_factor = 1.0 + (infestation_rate * 10) 
            dying_bees = int(dying_bees * viral_collapse_factor)
            
        # 5. Food Consumption
        daily_consumption = current_bees * 0.00002 # kg per bee per day
        food = max(0, food - daily_consumption)
        if food <= 0:
            # Starvation collapse
            dying_bees = int(current_bees * 0.5)
            
        # Update State
        current_bees = max(0, current_bees + new_bees - dying_bees)
        
        status = "Healthy"
        if current_bees == 0:
            status = "Colony Collapse (Dead)"
        elif infestation_rate > 0.05:
            status = "Critical DWV Outbreak"
        elif food < 2:
            status = "Starvation Risk"
            
        timeline.append(SimulationResult(
            day=day,
            bee_population=current_bees,
            varroa_population=current_varroa,
            food_stores_kg=round(food, 2),
            status=status
        ))
        
        if current_bees == 0:
            break
            
    return timeline

@app.post("/api/simulate-hive", response_model=list[SimulationResult])
def run_simulation(state: HiveState):
    """
    Combines deterministic biology with local GGUF anomalies (in full prod).
    """
    return simulate_30_days(state)

if __name__ == "__main__":
    # Test simulation
    test_state = HiveState(
        bee_population=40000,
        varroa_population=2000, # 5% starting infestation (Critical)
        queen_age_months=12,
        food_stores_kg=10.0,
        user_action="Applied Formic Pro"
    )
    res = simulate_30_days(test_state)
    print(f"Day 30 Status: {res[-1].status}, Bees: {res[-1].bee_population}, Varroa: {res[-1].varroa_population}")
