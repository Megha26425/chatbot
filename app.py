import streamlit as st
import google.generativeai as g
import os, requests
from dotenv import load_dotenv
from supabase import create_client, Client
from datetime import datetime

# supabse
def upload_to_supabase(username):
    load_dotenv()
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    supabase: Client = create_client(url, key)

    user_session = st.session_state.user.session
    supabase.auth.set_session(
        access_token=user_session.access_token,
        refresh_token=user_session.refresh_token
    )

    file_path = f"chat_logs/{username}.txt"
    with open(file_path, "rb") as f:
        supabase.storage.from_("chatlogs").upload(
            f"{username}.txt",
            f,
            {
                "x-upsert": "true",
                "cache-control": "3600"
            }
        )

#load it into a list, rest done in login.
def load_chat_history(username):
    file_path = f"chat_logs/{username}.txt" #the txt file
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            messages = []
            for i in range(0, len(lines), 2):
                if i + 1 < len(lines):
                    q = lines[i].replace("user: ", "").strip() 
                    a = lines[i + 1].strip()
                    source = "Gemini" if a.startswith("gemini:") else "DeepSeek"
                    messages.append((q, a.split(": ", 1)[1], source))
            return messages
    return []

def show():
    load_dotenv()

    st.title("MyChatBot")
    st.write("Welcome! Ask me anything below.")

    if "flag" not in st.session_state:
        st.session_state.flag = 0  

    if "messages" not in st.session_state:
        st.session_state.messages = []

    username = st.session_state.get("username", "guest")
    file_path = f"chat_logs/{username}.txt"
    os.makedirs("chat_logs", exist_ok=True)

    with st.container():
        with st.form("chat_form", clear_on_submit=True): 
            ip = st.text_input("Enter your query...", key="user_input")
            submitted = st.form_submit_button("Send")

    if submitted and ip.strip():
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        #gemini if true else deep
        if st.session_state.flag:
            st.session_state.messages.append((ip, " Generating response...", "Gemini"))
            g.configure(api_key=os.getenv("ApiKey"))
            model = g.GenerativeModel("models/gemini-1.5-flash")
            chat = model.start_chat()
            response = chat.send_message(ip)
            bot = response.text
            st.session_state.messages[-1] = (ip, bot, "Gemini")
        else:
            st.session_state.messages.append((ip, " Generating response...", "DeepSeek"))
            DAPI_KEY = os.getenv("DapiKey")
            headers = {
                "Authorization": f"Bearer {DAPI_KEY}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": ip}
                ]
            }
            response = requests.post(
                "https://api.deepseek.com/v1/chat/completions",
                headers=headers,
                json=payload
            )
            if response.status_code == 200:
                bot = response.json()["choices"][0]["message"]["content"]
            else:
                bot = f"Error: {response.status_code}\n{response.text}"

            st.session_state.messages[-1] = (ip, bot, "DeepSeek")

        with open(file_path, "a", encoding="utf-8") as f:
            f.write(f"user: {ip}\n")
            f.write(f"{st.session_state.messages[-1][2].lower()}: {bot}\n")

        upload_to_supabase(username)

    #list[index] => 0: g and 1: d;;;
    if st.button(f"Switch to {['Gemini', 'DeepSeek'][1 - st.session_state.flag]}"):
        st.session_state.flag = 1 - st.session_state.flag

    
    
    
