from dotenv import load_dotenv
import os
from pathlib import Path

# Force load .env from same folder as this file
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

GROQ_API_KEY = "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"
print("Loaded GROQ_API_KEY:", GROQ_API_KEY)


from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import whisper
import subprocess
import requests
import os

app = FastAPI()

# -----------------------------
# Enable CORS (for React)
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Load Whisper (LIGHT VERSION)
# -----------------------------
print("Loading Whisper...")
whisper_model = whisper.load_model("small")  # NOT medium
print("Whisper loaded.")

# -----------------------------
# Groq API Setup
# -----------------------------
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def generate_summary(transcript):

    if not GROQ_API_KEY:
        raise Exception("GROQ_API_KEY is not set!")

    print("Using GROQ_API_KEY inside function:", GROQ_API_KEY)

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama-3.1-8b-instant",
        "messages": [
    {
        "role": "system",
        "content": "You are an expert at turning messy video transcripts into viral short-form content summaries."
    },
    {
        "role": "user",
        "content": f"""
Clean this transcript.
Fix broken words.
Remove filler.
Then give:
1. A clear summary
2. 3 viral hook ideas
3. 3 short clip titles

Transcript:
{transcript}
"""
    }
]

    }

    response = requests.post(url, headers=headers, json=data)

    print("Groq status:", response.status_code)
    print("Groq response:", response.text)

    return response.json()["choices"][0]["message"]["content"]


# -----------------------------
# Audio Extraction
# -----------------------------
def extract_audio(video_path):
    output_audio = "audio.wav"

    command = [
        "ffmpeg",
        "-i", video_path,
        "-vn",
        "-acodec", "pcm_s16le",
        "-ar", "16000",
        "-ac", "1",
        output_audio,
        "-y"
    ]

    subprocess.run(command)
    return output_audio

# -----------------------------
# API Endpoint
# -----------------------------
@app.post("/process-video/")
async def process_video(file: UploadFile = File(...)):

    video_path = file.filename

    with open(video_path, "wb") as f:
        f.write(await file.read())

    audio_path = extract_audio(video_path)

    transcript = whisper_model.transcribe(audio_path)["text"]

    summary = generate_summary(transcript)

    return {
        "transcript": transcript,
        "summary": summary
    }
