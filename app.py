from audio_utils import record_audio, transcribe_audio
from quiz_generator import load_text, generate_mcqs
from tts import speak_text
import streamlit as st
import tempfile
import re

st.set_page_config(page_title="🎤 Voice MCQ Quiz", layout="centered")
st.title("🎙️ Voice-Based MCQ Quiz")

# Initialize session state
if "mcqs" not in st.session_state:
    st.session_state.mcqs = []
    st.session_state.answer = None
    st.session_state.correct = None
    st.session_state.total = 0
    st.session_state.show_result = False

# File upload
uploaded_file = st.file_uploader("📄 Upload your MCQ file (PDF or TXT)", type=["pdf", "txt"])
if uploaded_file and not st.session_state.mcqs:
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(uploaded_file.read())
        file_path = tmp.name

    st.success("✅ File uploaded successfully!")
    docs = load_text(file_path)
    full_mcq_text = generate_mcqs(docs[0].page_content)

    mcqs = full_mcq_text.strip().split("\n\n")[:1]  # Limit to first question
    st.session_state.mcqs = mcqs
    st.session_state.total = len(mcqs)
    st.session_state.answer = None
    st.session_state.correct = None
    st.session_state.show_result = False
    st.success("🎯 MCQ Quiz is ready with 1 question!")

# Show result
if st.session_state.show_result:
    question_block = st.session_state.mcqs[0]
    match = re.search(r"Answer:\s*\(?([A-Da-d])\)?", question_block)
    correct_option = match.group(1).upper() if match else "?"
    user_answer = st.session_state.answer

    st.markdown("### 📊 Result")
    st.markdown(f"- Your Answer: {user_answer}")
    st.markdown(f"- Correct Answer: {correct_option}")

    if user_answer == correct_option:
        st.success("✅ Correct!")
        speak_text("Correct")
    else:
        st.error("❌ Incorrect")
        speak_text("Incorrect")

    if st.button("🔁 Try Another Question"):
        st.session_state.clear()
        st.rerun()

# Ask question
if st.session_state.mcqs and not st.session_state.show_result:
    question_block = st.session_state.mcqs[0]
    match = re.search(r"Answer:\s*\(?([A-Da-d])\)?", question_block)
    correct_option = match.group(1).upper() if match else "?"
    question_display = re.sub(r"\n?Answer:.*", "", question_block)

    st.markdown("### ❓ Question")
    st.text(question_display)
    speak_text("Question")
    speak_text(question_display)

    st.info("🎙️ Recording your voice answer...")
    with st.spinner("Listening..."):
        audio_file = record_audio(duration=3)

    if audio_file:
        with st.spinner("Transcribing..."):
            voice_text = transcribe_audio(audio_file)

        st.write(f"🗣️ You said: `{voice_text}`")

        voice_text_cleaned = voice_text.strip().lower().replace(".", "").replace(",", "")
        mapping = {
            "a": ["a", "ay", "ae", "hey"],
            "b": ["b", "bee", "be", "bi"],
            "c": ["c", "see", "sea", "si", "yes"],
            "d": ["d", "dee", "di", "de"]
        }

        matched = None
        for letter, variants in mapping.items():
            if any(variant in voice_text_cleaned for variant in variants):
                matched = letter.upper()
                break

        if matched:
            st.session_state.answer = matched
            st.session_state.correct = (matched == correct_option)
            st.session_state.show_result = True
            st.rerun()
        else:
            st.warning("⚠️ Could not detect A, B, C, or D in your answer. Please try again.")
