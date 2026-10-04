import pyaudio
import wave
import os
import numpy as np
#from faster_whisper import WhisperModel

class Ears:
    def listen(self):
        print("Voice input disabled — placeholder active.")
        return ""


#class SpeechToText:
    def __init__(self, model_size="tiny.en"):
        # Load whisper locally on CPU (use device="cuda" if you have an NVIDIA GPU)
        #self.model = WhisperModel(model_size, device="cpu", compute_type="int8")
        self.RATE = 16000
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1

    def record_audio(self, output_filename="temp_command.wav", timeout=5, max_silence=2):
        """Records voice command right after wake word detection."""
        p = pyaudio.PyAudio()
        stream = p.open(format=self.FORMAT, channels=self.CHANNELS,
                        rate=self.RATE, input=True,
                        frames_per_buffer=self.CHUNK)

        print("\n🎤 Listening for command...")
        frames = []
        silent_chunks = 0
        threshold = 500  # Silence threshold

        for _ in range(0, int(self.RATE / self.CHUNK * timeout)):
            data = stream.read(self.CHUNK, exception_on_overflow=False)
            frames.append(data)
            
            # Simple Silence Detection to auto-stop recording
            audio_data = np.frombuffer(data, dtype=np.int16)
            if np.abs(audio_data).mean() < threshold:
                silent_chunks += 1
            else:
                silent_chunks = 0

            if silent_chunks > int(self.RATE / self.CHUNK * max_silence) and len(frames) > 15:
                break

        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(output_filename, 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(p.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

        return output_filename

    def transcribe(self, audio_file="temp_command.wav") -> str:
        """Transcribes the recorded audio file into text."""
        segments, _ = self.model.transcribe(audio_file, beam_size=1)
        text = " ".join([segment.text for segment in segments]).strip()
        
        if os.path.exists(audio_file):
            os.remove(audio_file)
            
        return text
    
    