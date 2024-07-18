import whisper
from deep_translator import GoogleTranslator
import pyttsx3
from langdetect import detect, DetectorFactory
import pyaudio
import wave
import tempfile
import os

# Load the Whisper model
model = whisper.load_model("medium")

# Ensure consistent language detection results
DetectorFactory.seed = 0

#Function to record user audio
def record_audio(record_seconds=5):
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
    frames = []
    print("Record started")
    try:
        for _ in range(0, int(44100 / 1024 * record_seconds)):
            data = stream.read(1024)
            frames.append(data)
    except KeyboardInterrupt:
        pass
    print("Record stopped")
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    # Save the recorded audio to a temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    wf = wave.open(temp_file.name, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(44100)
    wf.writeframes(b''.join(frames))
    wf.close()

    return temp_file.name

# Function to transcribe audio
def transcribe_audio(file_path):
    try:
        result = model.transcribe(file_path)
        return result["text"]
    except Exception as e:
        print(f"Error in transcription: {e}")
        return 'An error occured in transcription'

# Function to translate text using deep_translator's GoogleTranslator service
def translate_text(text, target_language="en"):
    try:
        #If the target language is the same as the original language, no need to translate
        if detect(text)==target_language:
            return text
        else:
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
            print("No matching voice found, using default voice.")
            engine.setProperty('voice', voices[0].id)
            selected_voice = voices[0].name

        print(f"*Using voice: {selected_voice}")
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Error in text to speech: {e}")

# Function to delete the temporary audio file
def delete_temp_file(file_path):
    try:
        os.remove(file_path)
        print(f"Temporary file {file_path} deleted successfully.")
    except Exception as e:
        print(f"Error deleting temporary file {file_path}: {e}")


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
    print(f"Transcribed Text: {transcribed_text}")

    #Play the transcripted text
    text_to_speech(transcribed_text, lang=detect(transcribed_text))
    print("**Transcripted text played.")

    # Translate text
    translated_text = translate_text(transcribed_text, target_language=target_lang)
    print(f"Translated Text: {translated_text}")

    # Convert translated text to speech and play it
    text_to_speech(translated_text, lang=target_lang)
    print("**Translated text played.")


if __name__ == "__main__":
    try:
        path = record_audio(record_seconds=7)
        main(path)
        delete_temp_file(path)
    except Exception as e:
        print("An error occurred:", e)