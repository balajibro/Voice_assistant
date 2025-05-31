import pvporcupine
import pyaudio
import struct
import speech_recognition as sr
import pyttsx3
import requests
from bs4 import BeautifulSoup
import subprocess
import os
import time

# === Text-to-Speech ===
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# === Speech-to-Text ===
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio).lower()
    except sr.UnknownValueError:
        return "Sorry, I didn't catch that."
    except sr.RequestError:
        return "Speech recognition error."

# === GPT from Ollama (LLaMA3 or Mistral etc) ===
def gpt_local(prompt):
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "llama3",  # Can change to 'mistral' or others
        "prompt": prompt,
        "stream": False
    }
    try:
        response = requests.post(url, json=payload)
        return response.json()["response"]
    except Exception as e:
        return f"Error from GPT: {str(e)}"

# === Free Web Search (DuckDuckGo) ===
def web_search(query):
    try:
        url = f"https://html.duckduckgo.com/html?q={query.replace(' ', '+')}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        results = soup.find_all('a', class_='result__a')
        if results:
            return f"Search result: {results[0].text}"
        else:
            return "No results found."
    except Exception as e:
        return f"Web search failed: {str(e)}"

# === Process Commands ===
def handle_command(command):
    if "search" in command:
        query = command.replace("search", "").strip()
        return web_search(query)
    elif "exit" in command or "quit" in command:
        speak("Goodbye!")
        exit()
    else:
        return gpt_local(command)

# === Main Assistant After Wake Word ===
def run_assistant():
    speak("How can I help you?")
    command = listen()
    print(f"🧠 Command: {command}")
    response = handle_command(command)
    print(f"🤖: {response}")
    speak(response)

# === Wake Word Listener ===
def listen_for_wake_word():
    porcupine = pvporcupine.create(keywords=["jarvis"])
    pa = pyaudio.PyAudio()
    stream = pa.open(format=pyaudio.paInt16,
                     channels=1,
                     rate=16000,
                     input=True,
                     frames_per_buffer=porcupine.frame_length)

    print("🕵️ Waiting for wake word...")

    try:
        while True:
            pcm = stream.read(porcupine.frame_length, exception_on_overflow=False)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
            if porcupine.process(pcm) >= 0:
                print("🎉 Wake word detected!")
                run_assistant()
                time.sleep(1)  # prevent double triggering
    except KeyboardInterrupt:
        print("Stopping wake listener...")
    finally:
        stream.stop_stream()
        stream.close()
        pa.terminate()
        porcupine.delete()

# === Entry Point ===
if __name__ == "__main__":
    listen_for_wake_word()
