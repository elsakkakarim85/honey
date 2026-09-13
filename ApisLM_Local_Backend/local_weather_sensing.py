import openmeteo_requests
import requests_cache
from retry_requests import retry

def get_open_meteo_client():
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    return openmeteo_requests.Client(session=retry_session)

def calculate_foraging_score(temperature, wind_speed, precipitation):
    """
    Algorithm to predict optimal nectar flow days.
    Penalizes winds > 20km/h, requires temp > 15C, and no rain.
    Returns a score from 0 to 100.
    """
    score = 100
    
    # Temperature penalty
    if temperature < 15.0 or temperature > 38.0:
        score -= 50
    elif temperature < 18.0:
        score -= 20
        
    # Wind penalty
    if wind_speed > 30.0:
        score -= 80
    elif wind_speed > 20.0:
        score -= 40
        
    # Precipitation penalty
    if precipitation > 0:
        score -= (precipitation * 20) # Heavy penalty for rain
        
    return max(0, min(100, int(score)))

def fetch_microclimate(lat: float, lon: float):
    print(f"Fetching Zero-Cost Remote Sensing Data for GPS: {lat}, {lon}")
    client = get_open_meteo_client()
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": ["temperature_2m", "relative_humidity_2m", "wind_speed_10m", "precipitation", "soil_moisture_0_to_1cm"],
        "forecast_days": 1
    }
    
    responses = client.weather_api(url, params=params)
    response = responses[0]
    
    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
    hourly_wind_speed_10m = hourly.Variables(2).ValuesAsNumpy()
    hourly_precipitation = hourly.Variables(3).ValuesAsNumpy()
    
    # Calculate average foraging score for daylight hours (simulated as middle of the array)
    avg_temp = float(hourly_temperature_2m[12])
    avg_wind = float(hourly_wind_speed_10m[12])
    avg_precip = float(hourly_precipitation[12])
    
    score = calculate_foraging_score(avg_temp, avg_wind, avg_precip)
    
    return {
        "latitude": lat,
        "longitude": lon,
        "current_temp_c": round(avg_temp, 2),
        "current_wind_kmh": round(avg_wind, 2),
        "current_precipitation_mm": round(avg_precip, 2),
        "optimal_foraging_score": score
    }

if __name__ == "__main__":
    result = fetch_microclimate(45.123, 9.456)
    print("Microclimate Result:", result)
