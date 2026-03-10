import speech_recognition as sr
from pydub import AudioSegment
import os

def speech_to_text(audio_file):

    # Convert uploaded audio to WAV
    sound = AudioSegment.from_file(audio_file)
    wav_file = "temp_audio.wav"
    sound.export(wav_file, format="wav")

    recognizer = sr.Recognizer()

    with sr.AudioFile(wav_file) as source:
        audio = recognizer.record(source)

    text = recognizer.recognize_google(audio)

    return text