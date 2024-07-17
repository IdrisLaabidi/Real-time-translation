import whisper
from deep_translator import GoogleTranslator
import pyttsx3
from langdetect import detect, DetectorFactory
import logging



# Load the Whisper model
model = whisper.load_model("base")

# Ensure consistent language detection results
DetectorFactory.seed = 0

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to transcribe audio
def transcribe_audio(file_path):
    try:
        result = model.transcribe(file_path)
        return result["text"]
    except Exception as e:
        logging.error(f"Error in transcription: {e}")
        return 'An error occured in transcription'

# Function to translate text using deep_translator's LibreTranslate service
def translate_text(text, target_language="en"):
    try:
        #If the target language is the same as the original language, no need to translate
        if detect(text)==target_language:
            return text
        else:
            translator = GoogleTranslator(source='auto', target=target_language)
            return translator.translate(text)
    except Exception as e :
        logging.error(f"Error in translation: {e}")
        return text

#Function to convert text to speech and play it
def text_to_speech(text, lang='en'):
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')

        # Print available voices in the computer and their languages
        '''for voice in voices:
            logging.info(f"Voice: {voice.name}")'''
        
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
            logging.warning("No matching voice found, using default voice.")
            engine.setProperty('voice', voices[0].id)
            selected_voice = voices[0].name

        logging.info(f"*Using voice: {selected_voice}")
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        logging.error(f"Error in text to speech: {e}")


def main(path):
    lang=('fr', 'en', 'ru', 'de')
    while True:
        choice = int(input("Choose a language to translate the speech: \n1. French \n2. English \n3. Russian \n4.German\n"))
        if (0<choice<=len(lang)):
            target_lang = lang[choice-1]
            break
        else:
            logging.warning("You must choose a number between 1 and 4!\n")
    # Transcribe audio
    transcribed_text = transcribe_audio(path)
    logging.info(f"Transcribed Text: {transcribed_text}")

    #Play the transcripted text
    text_to_speech(transcribed_text, lang=detect(transcribed_text))
    logging.info("**Transcripted text played.")

    # Translate text
    translated_text = translate_text(transcribed_text, target_language=target_lang)
    logging.info(f"Translated Text: {translated_text}")

    # Convert translated text to speech and play it
    text_to_speech(translated_text, lang=target_lang)
    logging.info("**Translated text played.")


if __name__ == "__main__":
    try:
        #path = 'RU_F_DashaCH.mp3'
        path='FRE_M_LaurentG.mp3'
        main(path)
    except Exception as e:
        logging.error("An error occurred:", e)