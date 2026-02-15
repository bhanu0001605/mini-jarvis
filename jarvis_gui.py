import tkinter as tk
from tkinter import scrolledtext
import datetime
import json
import os
import webbrowser
import subprocess

# ================= MEMORY SYSTEM =================

FILE = "memory.json"

if os.path.exists(FILE):
    with open(FILE, "r") as f:
        memory = json.load(f)
else:
    memory = {}

def save_memory():
    with open(FILE, "w") as f:
        json.dump(memory, f)

# ================= AI LOGIC =================

def get_response(user):

    user = user.lower()

    if user == "bye":
        return "Goodbye Darling 🔥"

    elif "time" in user:
        now = datetime.datetime.now().strftime("%H:%M:%S")
        return "Current time is " + now

    elif "my name is" in user:
        name = user.replace("my name is", "").strip()
        memory["name"] = name
        save_memory()
        return "Nice to meet you " + name

    elif "what is my name" in user:
        if "name" in memory:
            return "Your name is " + memory["name"]
        else:
            return "I don't know your name yet."

    elif "open google" in user:
        webbrowser.open("https://www.google.com")
        return "Opening Google"

    elif "open notepad" in user:
        subprocess.Popen("notepad.exe")
        return "Opening Notepad"

    elif "open calculator" in user:
        subprocess.Popen("calc.exe")
        return "Opening Calculator"

    elif user in memory:
        return memory[user]

    else:
        return "I don't know that. Teach me."

# ================= GUI SYSTEM =================

def send_message():
    user = entry.get().strip()
    chat_area.insert(tk.END, "You: " + user + "\n")

    response = get_response(user)

    if response == "I don't know that. Teach me.":
        chat_area.insert(tk.END, "Jarvis: Teach me the correct reply.\n")
        entry.delete(0, tk.END)
        return

    chat_area.insert(tk.END, "Jarvis: " + response + "\n")
    entry.delete(0, tk.END)

def teach_message():
    user = entry.get().strip()
    last_line = chat_area.get("end-3l", "end-2l").strip()

    if "You:" in last_line:
        question = last_line.replace("You:", "").strip()
        memory[question] = user
        save_memory()
        chat_area.insert(tk.END, "Jarvis: Learned successfully ✅\n")
        entry.delete(0, tk.END)

# ================= MAIN WINDOW =================

window = tk.Tk()
window.title("Mini Jarvis Assistant")
window.geometry("500x550")
window.configure(bg="#1e1e1e")

chat_area = scrolledtext.ScrolledText(
    window,
    wrap=tk.WORD,
    bg="#2b2b2b",
    fg="white",
    insertbackground="white"
)
chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

entry = tk.Entry(window, bg="#2b2b2b", fg="white", insertbackground="white")
entry.pack(padx=10, pady=5, fill=tk.X)

send_button = tk.Button(
    window,
    text="Send",
    bg="#3a3a3a",
    fg="white",
    command=send_message
)
send_button.pack(pady=5)

teach_button = tk.Button(
    window,
    text="Teach",
    bg="#444444",
    fg="white",
    command=teach_message
)
teach_button.pack(pady=5)

window.mainloop()
