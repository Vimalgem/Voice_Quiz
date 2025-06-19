# Voice-Based MCQ Quiz App

This project is a Streamlit web application that generates multiple-choice questions (MCQs) from uploaded PDF or TXT documents and conducts a voice-based quiz. Users can answer each question using their voice, and the app uses OpenAI's Whisper model for speech recognition.

---

## Features

* 📄 Upload your own PDF or TXT documents.
* 🧠 Uses GPT-3.5 to generate MCQs from text content.
* 🗣️ Answers are given by voice using a microphone.
* ✅ Instant feedback on whether the answer was correct.
* 🔁 Restart the quiz with a new document or questions.

---

## Technologies Used

* **Streamlit**: Web UI
* **OpenAI Whisper**: Voice transcription
* **LangChain + OpenAI (GPT-3.5)**: Question generation
* **Text-to-Speech (TTS)**: Uses pyttsx3 or similar

---

## How It Works

1. User uploads a `.pdf` or `.txt` file.
2. The document is parsed and chunked using LangChain.
3. GPT generates MCQs using a prompt template.
4. One question is shown at a time.
5. User speaks the answer (e.g., "A", "B", etc.).
6. The app transcribes it using Whisper and checks correctness.
7. Final score is displayed at the end.

---

## Requirements

```bash
pip install streamlit openai whisper sounddevice scipy numpy langchain python-dotenv chardet
```

Also, install FFmpeg and set its path:

```bash
# Example on Windows:
Set Environment Variable:
C:\ffmpeg\bin
```

---

## Running the App

```bash
streamlit run app.py
```

Make sure your `OPENAI_API_KEY` is stored in a `.env` file:

```
OPENAI_API_KEY=your_openai_key_here
```

---

## File Structure

```
voice_quiz_app/
├── app.py                  # Main Streamlit app
├── audio_utils.py          # Audio recording & Whisper transcription
├── quiz_generator.py       # LangChain & GPT-based MCQ generator
├── .env                    # API key
├── requirements.txt        # Optional: dependencies
```

---

## Example MCQ Format (Generated)

```
1. What is Python known for?
(a) Being a compiled language.
(b) Being an interpreted, high-level language.
(c) Being a low-level language.
(d) Being a markup language.
Answer: (b)
```

---

## Troubleshooting

* ❗ Whisper requires FFmpeg to be correctly installed.
* ❗ Make sure your microphone permission is granted.
* ❗ Voice should clearly include "A", "B", "C", or "D".

---

## License

MIT License
