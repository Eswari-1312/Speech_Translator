from gtts import gTTS

def text_to_speech(text, lang, output_path):
    tts = gTTS(text=text, lang=lang)
    tts.save(output_path)