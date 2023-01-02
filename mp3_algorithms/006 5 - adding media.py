import streamlit as st 

# Images

from PIL import Image

img = Image.open("st.jpg")

st.image(img)

#st.image("")

# Video

video1 = open("Day83.mp4", "rb")

st.video(video1, start_time = 25)

# Audio

audio1 = open("audio.mp3", "rb")

st.audio(audio1)