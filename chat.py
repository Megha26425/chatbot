import google.generativeai as g
import os

from dotenv import load_dotenv
load_dotenv()

g.configure(api_key = os.getenv("ApiKey"))

model = g.GenerativeModel("models/gemini-1.5-flash")

chat = model.start_chat()

history = []

while True:
  ip = input("enter: ")

  if ip.lower()=="quit" or ip.lower()=="exit":
    with open("hist.txt", "a") as file:
      file.writelines(history)
    break



  response = chat.send_message(ip)
  bot = response.text
  print(bot)

  history.append("user: "+ip+"\n")
  history.append("bot: "+bot+"\n")



