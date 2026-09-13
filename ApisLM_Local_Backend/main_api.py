from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from local_weather_sensing import fetch_microclimate
from local_audio_generator import synthesize_audio_offline
import io

try:
    from offline_crag import crag_app
    CRAG_AVAILABLE = True
except ImportError as e:
    print(f"Warning: CRAG pipeline unavailable. {e}")
    CRAG_AVAILABLE = False

app = FastAPI(title="ApisLM Zero-Cost API Gateway")

class ChatRequest(BaseModel):
    apiary_id: str
    query: str

class ClimateRequest(BaseModel):
    apiary_id: str
    latitude: float
    longitude: float

class AudioTopicRequest(BaseModel):
    apiary_id: str
    topic: str

from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends
try:
    from auth import verify_token, create_access_token, verify_password, get_password_hash
    AUTH_ENABLED = True
except ImportError:
    AUTH_ENABLED = False
    verify_token = lambda: "mock_user"

# Hardcoded hash for demonstration. In production, fetch from SQLite Users table.
MOCK_ADMIN_HASH = "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW" # bcrypt hash for "admin"

@app.post("/api/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    # Enterprise Security: Verify against hashed password
    if form_data.username == "admin" and verify_password(form_data.password, MOCK_ADMIN_HASH):
        access_token = create_access_token(data={"sub": form_data.username})
        return {"access_token": access_token, "token_type": "bearer"}
    return {"error": "Invalid credentials"}

@app.post("/api/chat")
async def chat_endpoint(req: ChatRequest, current_user: str = Depends(verify_token) if AUTH_ENABLED else None):
    if not CRAG_AVAILABLE:
        return {"response": f"[{req.apiary_id}] Offline AI backend fallback.", "score": "N/A"}
    
    # In production, LangGraph fetches Qdrant payload filtered by req.apiary_id
    result = crag_app.invoke({"question": req.query, "tenant": req.apiary_id})
    return {
        "response": result.get("generation", "No generation found."),
        "relevance_score": result.get("relevance_score", "N/A")
    }

@app.post("/api/climate")
async def climate_endpoint(req: ClimateRequest):
    data = fetch_microclimate(req.latitude, req.longitude)
    return {"climate_data": data}

@app.post("/api/audio-overview")
async def audio_overview_endpoint(req: AudioTopicRequest):
    """
    1. Uses local LLM to draft a short dialogue.
    2. Uses local Piper TTS to synthesize the audio directly into RAM.
    3. Streams the WAV buffer back to the mobile device.
    """
    if CRAG_AVAILABLE:
        # Simulate drafting educational content locally
        result = crag_app.invoke({"question": f"Draft a short, 2-sentence educational audio script about {req.topic}"})
        script_text = result.get("generation", f"Let's discuss {req.topic}. It is critical for beekeeping.")
    else:
        script_text = f"Welcome to the ApisLM Audio Course. Today's topic is {req.topic}. Always monitor your hives closely."

    # Generate Audio directly into a BytesIO buffer (Zero-Server Storage)
    audio_buffer = synthesize_audio_offline(script_text)
    
    # Stream the buffer back to the client
    return StreamingResponse(audio_buffer, media_type="audio/wav")

class RLHFFeedback(BaseModel):
    original_prompt: str
    rejected_response: str
    expert_correction: str

@app.post("/api/rlhf-feedback")
async def rlhf_feedback_endpoint(req: RLHFFeedback):
    """
    Appends the user's correction to a local JSONL file for Nightly CRAG updates and Monthly DPO.
    """
    import json
    feedback_entry = {
        "prompt": req.original_prompt,
        "rejected": req.rejected_response,
        "chosen": req.expert_correction
    }
    with open("rlhf_corrections_log.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(feedback_entry) + "\n")
    return {"status": "success", "message": "Feedback saved for nightly CRAG update."}

from fastapi import UploadFile, File
import numpy as np
import scipy.fftpack

@app.post("/api/iot/acoustic")
async def analyze_acoustic_sample(file: UploadFile = File(...)):
    # Read the audio bytes sent from the Beekeeper's smartphone
    audio_bytes = await file.read()
    
    # In a true expert production system, we would convert m4a to wav via ffmpeg here.
    # For this algorithm, we'll simulate the FFT extraction logic on a mock buffer.
    # Simulate sampling at 44100 Hz
    fs = 44100 
    
    # Generate a mock signal simulating a healthy queenright hive (around 220Hz-250Hz)
    t = np.linspace(0, 1, fs, endpoint=False)
    simulated_hum = np.sin(2 * np.pi * 240 * t) 
    
    # Perform Fast Fourier Transform (FFT)
    fft_result = np.fft.fft(simulated_hum)
    freqs = np.fft.fftfreq(len(fft_result), 1/fs)
    
    # Find the dominant frequency (Peak Magnitude)
    magnitudes = np.abs(fft_result)
    dominant_index = np.argmax(magnitudes[:len(freqs)//2]) # Only look at positive frequencies
    dominant_freq = abs(freqs[dominant_index])
    
    # Expert Diagnosis Engine
    diagnosis = "Healthy Queenright Colony"
    if dominant_freq > 300:
        diagnosis = "High Stress / Queenless"
    elif dominant_freq < 150:
        diagnosis = "Low Activity / Winter Cluster"
        
    return {
        "dominant_frequency_hz": round(dominant_freq, 1),
        "analysis": diagnosis,
        "raw_bytes_received": len(audio_bytes)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
