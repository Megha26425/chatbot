import streamlit as st
import google.generativeai as g
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# App title
st.title("MyChatBot")
st.write("Welcome! Ask me anything:")

# Initialize session state for mode switching
if "flag" not in st.session_state:
    st.session_state.flag = 0  # 0 = DeepSeek, 1 = Gemini

# Mode names
mod = ["deepseek", "gemini"]

# User input
ip = st.text_input("Enter your query...")

# Gemini Mode
if st.session_state.flag:
    st.write("Using Gemini")

    g.configure(api_key=os.getenv("ApiKey"))
    model = g.GenerativeModel("models/gemini-1.5-flash")
    chat = model.start_chat()

    if ip:
        response = chat.send_message(ip)
        bot = response.text

        st.write(f"**You:** {ip}")
        st.write(f"**Gemini reply:** {bot}")

        with open("hist.txt", "a", encoding="utf-8") as file:
            file.write("user: " + ip + "\n")
            file.write("gemini: " + bot + "\n")

# DeepSeek Mode
else:
    st.write("Using DeepSeek")

    DAPI_KEY = os.getenv("DapiKey")
    headers = {
        "Authorization": f"Bearer {DAPI_KEY}",
        "Content-Type": "application/json"
    }

    if ip:
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": ip}
        ]

        payload = {
            "model": "deepseek-chat",
            "messages": messages
        }

        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers=headers,
            json=payload
        )

        if response.status_code == 200:
            data = response.json()
            bot = data["choices"][0]["message"]["content"]
        else:
            bot = f"Error: {response.status_code}\n{response.text}"

        st.write(f"**You:** {ip}")
        st.write(f"**DeepSeek reply:** {bot}")

        with open("hist.txt", "a", encoding="utf-8") as file:
            file.write("user: " + ip + "\n")
            file.write("deepseek: " + bot + "\n")

# Switch model button
if st.button(f"Switch to {mod[1 - st.session_state.flag]}"):
    st.session_state.flag = 1 - st.session_state.flag
