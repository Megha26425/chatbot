from dotenv import load_dotenv
import streamlit as st
import os
import app
from supabase import create_client
from datetime import datetime

st.set_page_config(page_title="ChatBot Login")

#supabase 
load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)

#session state
if "user" not in st.session_state:
    st.session_state.user = None

#have made the login page dissappear once logged in.
if not st.session_state.user:
    st.title("ChatBot Login Portal")
    mode = st.radio("Choose mode", ["Login", "Signup"])
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if mode == "Signup":
        username = st.text_input("Choose a unique username") #this will be used for the txt file.. like username.txt to bring back chats
        if st.button("Sign Up"):
            if not email or not password or not username:
                st.warning("Please fill in all fields.")
            else:
                try:
                    check = supabase.table("users").select("*").eq("username", username).execute()
                    if check.data:
                        st.error("Username already taken. Please choose another.")
                    else:
                        res = supabase.auth.sign_up({"email": email, "password": password})
                        if res.user:
                            os.makedirs("chat_logs", exist_ok=True)
                            with open(f"chat_logs/{username}.txt", "w", encoding="utf-8") as f:
                                f.write("")

                            supabase.table("users").insert({
                                "email": email,
                                "username": username,
                                "chat_file": f"{username}.txt"
                            }).execute()

                            st.success("Signup successful! Check email and confirm >:)")
                        else:
                            st.error("Signup failed >:( ")
                except Exception as e:
                    st.error(f"Sign-up failed: {e}")

    if mode == "Login":
        if st.button("Login"):
            try:
                user = supabase.auth.sign_in_with_password({"email": email, "password": password})
                st.session_state.user = user

                info = supabase.table("users").select("*").eq("email", email).single().execute()
                username = info.data["username"]
                st.session_state.username = username
                st.session_state.chat_file = f"chat_logs/{info.data['chat_file']}"

                os.makedirs("chat_logs", exist_ok=True)
                local_path = f"chat_logs/{username}.txt"

                # download chat
                try:
                    res = supabase.storage.from_("chatlogs").download(f"{username}.txt")
                    with open(local_path, "wb") as f:
                        f.write(res)
                except Exception:
                    st.info("No previous chat found — starting fresh!")

                # load chat 
                from app import load_chat_history
                st.session_state.messages = load_chat_history(username) # from app.py

                st.success("Logged in!")
                st.rerun()
            except Exception as e:
                st.error(f"Login failed: {e}")


if st.session_state.user:
    st.subheader(f"Welcome, {st.session_state.user.user.email}") #can simply use the username too if i want.
    app.show()

    # logout butt. clean up later
    if st.button("Logout"):
        from app import upload_to_supabase
        upload_to_supabase(st.session_state.username)

        st.session_state.user = None
        st.session_state.username = None
        st.session_state.chat_file = None
        st.session_state.messages = []
        st.rerun()

    # history
    with st.container():
        st.subheader("Chat History")
        with st.expander("Click to view", expanded=True):
            for i, (msg_user, msg_bot, source) in enumerate(st.session_state.messages):
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
                st.markdown(f"**[{i+1}] You** ({timestamp}): {msg_user}")
                st.markdown(f"**{source}**: {msg_bot}")
                st.markdown("---")

