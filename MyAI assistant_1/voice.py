import subprocess, sys, os
import numpy as np
import sounddevice as sd

PIPER_BIN = "piper/piper.exe" if sys.platform == "win32" else "piper/piper"

def play_beep(frequency=880, duration=0.15, volume=0.3):
    """Generates and plays a quick notification beep (sine wave)."""
    samplerate = 22050
    t = np.linspace(0, duration, int(samplerate * duration), False)
    # Generate 880Hz sine wave (A5 note)
    tone = np.sin(2 * np.pi * frequency * t) * volume
    audio_array = tone.astype(np.float32)
    sd.play(audio_array, samplerate=samplerate)
    sd.wait()

def speak(text: str):
    process = subprocess.Popen(
        [PIPER_BIN, "--model", "piper/en_US-lessac-medium.onnx", "--output-raw"],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    pcm_bytes, _ = process.communicate(text.encode('utf-8'))
    if not pcm_bytes:
        print("Error: No audio data received from Piper.")
        return
    try:
        audio_array = np.frombuffer(pcm_bytes, dtype=np.int16)
        sd.play(audio_array, samplerate=22050)
        sd.wait()
    except Exception as e:
        print(f"Playback exception occurred: {e}")