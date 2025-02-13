import pyaudio
import wave
import ffmpeg
import asyncio
from shazamio import Shazam
import webbrowser
import yt_dlp
import time
import subprocess
import yt_dlp
import os

# Settings for recording
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 10  # Adjust listening duration
WAV_FILE = "recorded_audio.wav"
MP3_FILE = "recorded_audio.mp3"
LAST_SONG = None  # Stores the last detected song to avoid repeats

# Initialize PyAudio
audio = pyaudio.PyAudio()

def record_audio():
    """Records audio from the selected microphone and saves it as a WAV file."""
    print("🎤 Listening for a song...")

    p = pyaudio.PyAudio()  # Initialize a new PyAudio instance every time
    device_index = 2 # Set this to your correct microphone index

    try:
        stream = p.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        input_device_index=device_index,  # Use the correct mic
                        frames_per_buffer=CHUNK)

        frames = []
        for _ in range(int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)

        print("✅ Recording finished.")

        stream.stop_stream()
        stream.close()
        p.terminate()  # Close PyAudio after each recording

        with wave.open(WAV_FILE, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))

        print(f"📁 Audio saved as {WAV_FILE}")
    
    except OSError as e:
        print(f"❌ Microphone error: {e}")
        print("🔄 Retrying in 5 seconds...")
        time.sleep(5)



def convert_to_mp3():
    """Converts the recorded WAV file to MP3 using FFmpeg and auto-overwrites the file."""
    print("🎼 Converting to MP3...")
    ffmpeg.input(WAV_FILE).output(MP3_FILE, audio_bitrate='192k').overwrite_output().run()
    print(f"✅ Converted to {MP3_FILE} (Overwritten)")

async def identify_song():
    """Uses ShazamIO to identify the recorded song and return song details."""
    global LAST_SONG  # To avoid repeating the same song
    shazam = Shazam()
    result = await shazam.recognize_song(MP3_FILE)

    if 'track' in result:
        song = result['track']
        title = song['title']
        artist = song['subtitle']
        url = song['url']

        # Avoid repeating the same song
        if LAST_SONG == (title, artist):
            print("🔁 Same song detected, waiting for change...")
            return None, None

        LAST_SONG = (title, artist)

        print("\n🎵 **Song Identified:**")
        print(f"🎶 **Title:** {title}")
        print(f"🎤 **Artist:** {artist}")
        print(f"🔗 **Shazam URL:** {url}")

        return title, artist
    else:
        print("❌ No song identified.")
        return None, None


VLC_PATH = r"C:\Program Files\VideoLAN\VLC\vlc.exe"  # Update if necessary

def play_music_video(title, artist):
    """Searches YouTube for the music video and streams it in VLC fullscreen."""
    if title and artist:
        search_query = f"{title} {artist} official music video"
        print(f"🔎 Searching YouTube for: {search_query}")

        ydl_opts = {
            'quiet': True,
            'format': 'best',
            'default_search': 'ytsearch',
            'noplaylist': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch:{search_query}", download=False)
            if 'entries' in info and len(info['entries']) > 0:
                video_url = info['entries'][0]['url']
                print(f"🎬 Streaming: {title} by {artist} in VLC Fullscreen")

                # Play video in VLC without showing the URL
                subprocess.Popen(
                    f'"{VLC_PATH}" --fullscreen --network-caching=1000 --meta-title="{title} - {artist}" "{video_url}"',
                    shell=True,
                    cwd=os.path.dirname(VLC_PATH)  # Ensure VLC runs from its directory
                )
            else:
                print("❌ No music video found.")

# **Main Loop: Keep Listening Until Stopped**
if __name__ == "__main__":
    try:
        while True:
            record_audio()
            convert_to_mp3()
            title, artist = asyncio.run(identify_song())

            if title and artist:
                play_music_video(title, artist)

            # Wait before recording again (avoid continuous loops)
            time.sleep(3)  # Adjust delay to avoid too frequent checks

    except KeyboardInterrupt:
        print("\n🛑 Stopping the continuous listening.")
