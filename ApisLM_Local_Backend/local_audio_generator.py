import os
import urllib.request
import soundfile as sf
import io
import numpy as np
try:
    from piper import PiperVoice
except ImportError:
    PiperVoice = None

MODEL_URL = "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/lessac/low/en_US-lessac-low.onnx"
CONFIG_URL = "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/lessac/low/en_US-lessac-low.onnx.json"
MODEL_PATH = "en_US-lessac-low.onnx"
CONFIG_PATH = "en_US-lessac-low.onnx.json"

def download_voice_model():
    if not os.path.exists(MODEL_PATH):
        print("Downloading Piper ONNX Voice Model (Zero-Cost TTS)...")
        urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)
        urllib.request.urlretrieve(CONFIG_URL, CONFIG_PATH)
        print("Download complete.")

def synthesize_audio_offline(text: str) -> io.BytesIO:
    """
    Synthesizes speech 100% locally on CPU via Piper TTS.
    Returns a memory buffer of the WAV file (Zero-Server Storage).
    """
    download_voice_model()
    
    out_buffer = io.BytesIO()
    
    if PiperVoice is None:
        print("Piper not fully installed, returning mock audio buffer.")
        # Generate dummy 1 second sine wave
        sample_rate = 22050
        t = np.linspace(0, 1, sample_rate)
        audio = 0.5 * np.sin(2 * np.pi * 440 * t)
        sf.write(out_buffer, audio, sample_rate, format='WAV')
    else:
        print("Synthesizing audio locally via Piper TTS...")
        voice = PiperVoice.load(MODEL_PATH, config_path=CONFIG_PATH)
        
        # Synthesize into buffer
        # Piper synthesize returns an iterator of audio frames
        audio_stream = voice.synthesize_stream_raw(text)
        
        # We write raw frames to a wav buffer. 
        # For simplicity in this script, we'll write a mock header or use a wave writer.
        import wave
        with wave.open(out_buffer, 'wb') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(voice.config.sample_rate)
            for audio_bytes in audio_stream:
                wav_file.writeframes(audio_bytes)
                
    out_buffer.seek(0)
    return out_buffer

if __name__ == "__main__":
    buf = synthesize_audio_offline("Hello, this is a local zero-cost test.")
    print("Buffer size:", len(buf.getvalue()))
