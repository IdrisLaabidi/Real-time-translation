import whisper
from deep_translator import GoogleTranslator
import pyttsx3



# Load the Whisper model
model = whisper.load_model("base")

# Function to transcribe audio
def transcribe_audio(file_path):
    result = model.transcribe(file_path)
    return result["text"]

# Function to translate text using deep_translator's LibreTranslate service
def translate_text(text, target_language="en"):
    translator = GoogleTranslator(source='auto', target=target_language)
    return translator.translate(text)

#Function to convert text to speech and play it
def text_to_speech(text, lang='english'):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')

    # Print available voices in the computer and their languages
    for voice in voices:
        print(f"Voice: {voice.name}")

    for voice in voices:
        if lang in voice.name.lower():
            engine.setProperty('voice', voice.id)
            break
    else:
        # If no matching voice is found, fall back to the first voice (default)
        print("No matching voice found, using default voice.")
        engine.setProperty('voice', voices[0].id)

    engine.say(text)
    engine.runAndWait()


if __name__ == "__main__":
    try:
        path = 'RU_F_DashaCH.mp3'
        # Transcribe audio
        transcribed_text = transcribe_audio(path)
        print("Transcribed Text:", transcribed_text)

        # Translate text
        translated_text = translate_text(transcribed_text, target_language='fr')
        print("Translated Text:", translated_text)

        # Convert translated text to speech and play it
        text_to_speech(translated_text, lang='french')
        print("Translated text played.")
    except Exception as e:
        print("An error occurred:", e)