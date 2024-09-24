# utils.py in the 'api' directory

def record_audio(duration,file):
    import sounddevice as sd
    import soundfile as sf
    import numpy as np

    # Define the file path for saving the recording
    #filename = 'output.wav'
    filename = file
    # Set the audio properties
    samplerate = 44100  # Hertz
    channels = 2  # Stereo

    print(f"Recording for {duration} seconds...")
    myrecording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=channels, dtype='float64')
    sd.wait()  # Wait until the recording is finished
    sf.write(filename, myrecording, samplerate)
    print("Recording saved.")
