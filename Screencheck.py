import subprocess

VLC_PATH = r"C:\Program Files\VideoLAN\VLC\vlc.exe"

try:
    subprocess.run([VLC_PATH, "--version"])
    print("✅ VLC is working!")
except FileNotFoundError:
    print("❌ VLC not found. Check the path.")
