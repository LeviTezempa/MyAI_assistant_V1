import openwakeword
from openwakeword.model import Model
import pyaudio
import numpy as np

class WakeWordDetector:
    def __init__(self, model_path="Hey,_Alex_20260806_010638.onnx"):
        # Initialize openWakeWord ONNX model
        self.oww_model = Model(wakeword_models=[model_path], inference_framework="onnx")
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 16000
        self.CHUNK = 1280  # 80ms chunk
        self.audio = pyaudio.PyAudio()

    def listen_for_wake_word(self):
        stream = self.audio.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK
        )
        print("⚡ Waiting for wake word ('Hey Alex')...")

        try:
            while True:
                data = stream.read(self.CHUNK, exception_on_overflow=False)
                audio_data = np.frombuffer(data, dtype=np.int16)
                
                # Inference
                self.oww_model.predict(audio_data)
                
                for _, score in self.oww_model.prediction_buffer.items():
                    if score[-1] > 0.5:  # Detection threshold
                        print("✨ Wake word detected!")
                        return True
        finally:
            stream.stop_stream()
            stream.close()
if __name__ == "__main__":
    print("Wake‑word module running standalone.")

# Fallback stub for environments without openwakeword
class WakeWordDetector:
    def listen(self):
        print("Wake‑word listening disabled (stub mode).")
