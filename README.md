
Hello!!

Instructions:-
-- Get your API key, and type it out in the .env file.
-- Run login.py in terminal.
-- Give your input for sign up/sign in. Confirm mail.
-- History will be stored in USERNAME.txt (Doesn't matter, it'll be visible too)

# 🤖 MyChatBot: Gemini + DeepSeek Chat App

An intelligent chatbot built using **Streamlit** that allows users to switch between **Google Gemini 1.5 Flash** and **DeepSeek** LLMs seamlessly. Ask anything and get smart, real-time replies!

---

## 🧠 Features

- 🔄 Toggle between Gemini and DeepSeek chat models
- 🧵 Maintains response history in a local `hist.txt` file
- 🛡️ Uses `.env` for secure API key management
- 📦 Lightweight, clean Streamlit UI

---

## ⚙️ Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **APIs Used**:
  - Google Gemini 1.5 Flash (via `google.generativeai`)
  - DeepSeek API (`https://api.deepseek.com/v1/chat/completions`)
- **Other Tools**:
  - `dotenv` for environment variable handling
  - `requests` for API interaction

---


