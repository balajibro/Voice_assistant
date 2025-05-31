# 🤖 Personal Voice Assistant - "Jarvis"

This is a **fully offline, smart voice assistant** that:

- 🎙️ Listens for the wake word: **"Hey Jarvis"**
- 🧠 Responds using **local GPT-style models via Ollama (LLaMA 3)**
- 🌐 Does **free, unlimited web searches** using DuckDuckGo
- 🔊 Speaks responses with text-to-speech
- 🗣️ Understands your voice using Google Speech API
- 💻 Runs automatically on Windows startup (optional)

---

## 🧰 Features

✅ Works offline (no OpenAI or internet needed for GPT)  
✅ 100% free and private  
✅ Web search support via DuckDuckGo  
✅ One-file design for simplicity  
✅ Works on any modern laptop

---

## 📥 Download & Setup Instructions

### 1. ✅ Install Python (if not already installed)

Download Python 3.10+ from:  
👉 https://www.python.org/downloads/  
✅ Be sure to check **"Add Python to PATH"** during install!

---

### 2. ✅ Install Ollama (for GPT)

Download and install Ollama from:  
👉 https://ollama.com/download

Then download the model:

```bash
ollama run llama3
