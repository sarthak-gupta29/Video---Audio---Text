import streamlit as st
import speech_recognition as sr
import os
import subprocess
from pydub import AudioSegment


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
        return "Sorry, I was unable to understand the audio."
    except sr.RequestError as e:
        return f"An error occurred while processing the request: {e}"

# Streamlit UI
st.title("🎥 Video-->Audio-->Text")
st.write("Upload a video file, extract its audio, convert it into text.")

# File uploader for video
video_file = st.file_uploader("Select your video file :", type=["mp4", "avi", "mov", "mkv"])

if video_file is not None:
    # Display the uploaded video inside a container
    with st.container():
        st.markdown("<div class='video-container'><h4 class='section-header'>Uploaded Video</h4></div>", unsafe_allow_html=True)
        st.video(video_file)

    st.write("Extracting audio from the video... Please wait.")

    # Convert video to audio
    audio_path = video_to_audio(video_file)

    # Display the extracted audio as an audio player inside a container
    with st.container():
        st.markdown("<div class='audio-container'><h4 class='section-header'>Extracted Audio</h4></div>", unsafe_allow_html=True)
        audio_file = open(audio_path, "rb")
        st.audio(audio_file.read(), format="audio/wav")
        audio_file.close()

    st.write("Converting the audio to text... This might take a few seconds.")

    # Convert the extracted audio file to text
    result = audio_to_text(audio_path)

    # Display the transcribed text inside a container
    with st.container():
        st.markdown("<div class='text-container'><h4 class='section-header'>Transcribed Text</h4></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='transcription'>{result}</div>", unsafe_allow_html=True)

    # Cleanup extracted audio file
    if os.path.exists(audio_path):
        os.remove(audio_path)
