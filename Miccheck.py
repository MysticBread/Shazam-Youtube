import pyaudio

p = pyaudio.PyAudio()

print("\n🔎 **Available Audio Devices:**")
for i in range(p.get_device_count()):
    device_info = p.get_device_info_by_index(i)
    print(f"🎤 {i}: {device_info['name']} (Input: {device_info['maxInputChannels']})")

p.terminate()
