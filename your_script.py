import pyaudio
import wave

# Settings
FORMAT = pyaudio.paInt16  # 16-bit audio
CHANNELS = 1  # Mono recording
RATE = 44100  # Sample rate in Hz
CHUNK = 1024  # Buffer size
RECORD_SECONDS = 10  # Adjust as needed
OUTPUT_FILE = "recorded_audio.wav"

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Open audio stream
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

print("Recording...")

frames = []

# Record in chunks
for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)
    

print("Recording finished.")

# Stop and close the stream
stream.stop_stream()
stream.close()
audio.terminate()

# Save to a WAV file
with wave.open(OUTPUT_FILE, 'wb') as wf:
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))

print(f"Audio saved as {OUTPUT_FILE}")

import ffmpeg

def convert_to_mp3(input_file, output_file):
    ffmpeg.input(input_file).output(output_file).run()
    print(f"Converted to {output_file}")

convert_to_mp3("recorded_audio.wav", "recorded_audio.mp3")
