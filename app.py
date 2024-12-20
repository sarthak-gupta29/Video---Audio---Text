import streamlit as st
import speech_recognition as sr
import os
import subprocess
from pydub import AudioSegment

# Custom CSS for styling the UI
st.markdown("""
    <style>
    body {
        background-color: #FFEB3B; /* Yellow background */
        color: #003366; /* Dark Blue text */
    }
    .video-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 20px;
        border: 2px solid #e29600;
        padding: 10px;
        border-radius: 8px;
        background-color: #f5f5f5;
    }
    .audio-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 20px;
        border: 2px solid #e29600;
        padding: 10px;
        border-radius: 8px;
        background-color: #f5f5f5;
    }
    .text-container {
        margin-top: 30px;
        padding: 20px;
        background-color: #f5f5f5;
        border-radius: 8px;
        border: 2px solid #e29600;
    }
    .title {
        text-align: center;
        color: #003366;
    }
    h1, h2, h3, h4 {
        color: #003366; /* Dark blue headers */
    }
    </style>
""", unsafe_allow_html=True)

# Function to extract audio from video using ffmpeg
def video_to_audio(video_file):
    # Save the uploaded video file temporarily
    video_path = "temp_video.mp4"
    with open(video_path, "wb") as f:
        f.write(video_file.getbuffer())

    # Use ffmpeg to extract audio
    audio_path = "extracted_audio.wav"
    command = ["ffmpeg", "-i", video_path, "-vn", "-acodec", "pcm_s16le", "-ar", "44100", "-ac", "2", audio_path]
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Clean up the temporary video file
    os.remove(video_path)

    return audio_path

# Function to convert audio to text
def audio_to_text(audio_path):
    recognizer = sr.Recognizer()

    # Use AudioFile to read the audio from the file path
    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)

    try:
        # Convert audio to text using Google Speech Recognition
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Sorry, I could not understand the audio."
    except sr.RequestError as e:
        return f"Error with the request: {e}"

# Streamlit UI
st.title("🎥 Video --> Audio --> Text Converter")
st.write("Upload a video, extract its audio, convert it into text.")

# File uploader for video
video_file = st.file_uploader("Choose a video file", type=["mp4", "avi", "mov", "mkv"])

if video_file is not None:
    # Display the uploaded video inside a container
    with st.container():
        st.markdown("<div class='video-container'><h4>Uploaded Video</h4></div>", unsafe_allow_html=True)
        st.video(video_file)

    st.write("Extracting audio from video...")

    # Convert video to audio
    audio_path = video_to_audio(video_file)

    # Display the extracted audio as an audio player inside a container
    with st.container():
        st.markdown("<div class='audio-container'><h4>Extracted Audio</h4></div>", unsafe_allow_html=True)
        audio_file = open(audio_path, "rb")
        st.audio(audio_file.read(), format="audio/wav")
        audio_file.close()

    st.write("Converting audio to text...")

    # Convert the extracted audio file to text
    result = audio_to_text(audio_path)

    # Display the transcribed text inside a container
    with st.container():
        st.markdown("<div class='text-container'><h4>Transcribed Text</h4></div>", unsafe_allow_html=True)
        st.write(f"**{result}**")

    # Cleanup extracted audio file
    if os.path.exists(audio_path):
        os.remove(audio_path)
