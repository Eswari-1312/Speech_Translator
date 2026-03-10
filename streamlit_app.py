import streamlit as st
import os
import tempfile
from pydub import AudioSegment

from speech_to_text.stt import speech_to_text
from translation.translator import translate_text
from text_to_speech.tts import text_to_speech

# -------------------------------
# Streamlit Page Config
# -------------------------------
st.set_page_config(
    page_title="Indian Languages Audio Translator",
    layout="centered"
)

st.title("🎙️ Indian Languages Audio Translator")
st.caption("Upload any Indian language audio → Translate → Listen")

# -------------------------------
# Language Selection
# -------------------------------
LANGUAGE_MAP = {
    "English": "en",
    "Hindi": "hi",
    "Telugu": "te",
    "Tamil": "ta",
    "Kannada": "kn",
    "Malayalam": "ml",
    "Marathi": "mr",
    "Bengali": "bn"
}

target_language = st.selectbox(
    "Select Target Language",
    list(LANGUAGE_MAP.keys())
)

# -------------------------------
# Audio Upload
# -------------------------------
uploaded_file = st.file_uploader(
    "📂 Select Audio File",
    type=["wav", "mp3", "m4a"]
)

# -------------------------------
# Processing
# -------------------------------
if uploaded_file is not None:

    st.success("File uploaded successfully")

    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False) as temp_audio:
        temp_audio.write(uploaded_file.read())
        temp_audio_path = temp_audio.name

    # Convert to WAV (required for SpeechRecognition)
    wav_path = temp_audio_path + ".wav"

    audio = AudioSegment.from_file(temp_audio_path)
    audio.export(wav_path, format="wav")

    st.info("🔊 Processing audio... Please wait")

    try:
        # Speech to Text
        original_text = speech_to_text(wav_path)

        st.subheader("📝 Recognized Text")
        st.write(original_text)

        # Translation
        translated_text = translate_text(
            original_text,
            LANGUAGE_MAP[target_language]
        )

        st.subheader("🌍 Translated Text")
        st.write(translated_text)

        # Text to Speech
        output_audio_path = "translated_output.mp3"

        text_to_speech(
            translated_text,
            LANGUAGE_MAP[target_language],
            output_audio_path
        )

        st.subheader("🔊 Translated Audio")
        st.audio(output_audio_path)

        st.success("✅ Translation completed successfully")

    except Exception as e:
        st.error("❌ Error occurred")
        st.exception(e)

    finally:
        # Remove temporary files
        if os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)

        if os.path.exists(wav_path):
            os.remove(wav_path)