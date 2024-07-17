import whisper
from deep_translator import GoogleTranslator
import pyttsx3
from langdetect import detect, DetectorFactory




# Load the Whisper model
model = whisper.load_model("base")

# Ensure consistent language detection results
DetectorFactory.seed = 0

# Function to transcribe audio
def transcribe_audio(file_path):
    try:
        result = model.transcribe(file_path)
        return result["text"]
    except Exception as e:
        print(f"Error in transcription: {e}")
        return 'An error occured in transcription'

# Function to translate text using deep_translator's LibreTranslate service
def translate_text(text, target_language="en"):
    try:
        translator = GoogleTranslator(source='auto', target=target_language)
        return translator.translate(text)
    except Exception as e :
        print(f"Error in translation: {e}")
        return text

#Function to convert text to speech and play it
def text_to_speech(text, lang='en'):
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')

        # Print available voices in the computer and their languages
        '''for voice in voices:
            print(f"Voice: {voice.name}")'''
        
        # Manual mapping of voice names to languages
        voice_map = {
            'en': 'english',
            'fr': 'french',
            'ru': 'russian',
            'uk': 'russian',
            'de': 'german',
            'ar': 'arabic'
        }

        lang = voice_map.get(lang)
        for voice in voices:
            if lang in voice.name.lower():
                engine.setProperty('voice', voice.id)
                selected_voice = voice.name
                break
        else:
            # If no matching voice is found, fall back to the first voice (default)
            print("No matching voice found, using default voice.")
            engine.setProperty('voice', voices[0].id)
            selected_voice = voices[0].name

        print(f"*Using voice: {selected_voice}")
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Error in text to speech: {e}")


def main(path):
    lang=('fr', 'en', 'ru', 'de')
    while True:
        choice = int(input("Choose a language to translate the speech: \n1. French \n2. English \n3. Russian \n4.German\n"))
        if (0<choice<=len(lang)):
            target_lang = lang[choice-1]
            break
        else:
            print("You must choose a number between 1 and 4!\n")
    # Transcribe audio
    transcribed_text = transcribe_audio(path)
    print("Transcribed Text:", transcribed_text)

    #Play the transcripted text
    text_to_speech(transcribed_text, lang=detect(transcribed_text))
    print("**Transcripted text played.")

    # Translate text
    translated_text = translate_text(transcribed_text, target_language=target_lang)
    print("Translated Text:", translated_text)

    # Convert translated text to speech and play it
    text_to_speech(translated_text, lang=target_lang)
    print("**Translated text played.")


if __name__ == "__main__":
    try:
        path = 'RU_F_DashaCH.mp3'
        main(path)
    except Exception as e:
        print("An error occurred:", e)