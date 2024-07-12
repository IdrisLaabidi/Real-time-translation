import whisper

# Load the Whisper model
model = whisper.load_model("base")

# Function to transcribe audio
def transcribe_audio(file_path):
    result = model.transcribe(file_path)
    return result["text"]

if __name__ == '__main__':
    path = './harvard.wav'
    print(transcribe_audio(path))