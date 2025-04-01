import os
import streamlit as st
import google.generativeai as genai
import PyPDF2

# Configure Gemini API
API_KEY = 'AIzaSyBNaLoA2ZlTD2bPVnR1HV4eRVmthDjnYos'
genai.configure(api_key=API_KEY)

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text

# Function to generate AI response
def get_ai_response(prompt):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

# Streamlit UI
st.set_page_config(page_title="ScholarAI", page_icon="📚", layout="wide")

st.title("📚 ScholarAI")
st.subheader("Your AI-Powered Learning Assistant")

# File Upload Section
uploaded_file = st.file_uploader("📂 Upload Lecture Notes (PDF/TXT)", type=["pdf", "txt"])

# Store the uploaded text content in session state to persist it across interactions
if uploaded_file:
    if uploaded_file.type == "application/pdf":
        text = extract_text_from_pdf(uploaded_file)
    else:
        text = uploaded_file.getvalue().decode("utf-8")

    st.session_state.text_content = text  # Store content in session state

    st.success("✅ File Uploaded Successfully!")

# Create a row for buttons
col1, col2, col3, col4 = st.columns(4)

# Buttons below the uploaded content
with col1:
    if st.button("📌 Summarize Notes"):
        with st.spinner("Generating Summary..."):
            summary = get_ai_response(f"Summarize the following notes:\n{st.session_state.text_content}")
        st.session_state.summary = summary  # Store the summary in session state
        st.markdown("### 📑 Summary")
        st.write(summary)

with col2:
    if st.button("🎯 Generate MCQs"):
        with st.spinner("Creating Questions..."):
            mcqs = get_ai_response(f"Generate 5 multiple-choice questions from the following:\n{st.session_state.text_content}")
        st.session_state.mcqs = mcqs  # Store the MCQs in session state
        st.markdown("### 📝 Quiz Questions")
        st.write(mcqs)

with col3:
    if st.button("🔖 Create Flashcards"):
        with st.spinner("Preparing Flashcards..."):
            flashcards = get_ai_response(f"Create 5 flashcards from the following:\n{st.session_state.text_content}")
        st.session_state.flashcards = flashcards  # Store the flashcards in session state
        st.markdown("### 🎓 Flashcards")
        st.write(flashcards)

with col4:
    query = st.text_input("🔍 Ask ScholarAI to explain a concept:")
    if st.button("🔍 Explain Concept"):
        if query.strip():
            with st.spinner("Thinking..."):
                result = get_ai_response(f"Explain {query} in simple terms.")
            st.session_state.explanation = result  # Store the explanation in session state
            st.markdown("### 📖 AI Explanation")
            st.write(result)
        else:
            st.error("⚠ Please enter a concept!")

# Display stored results when the corresponding button is clicked
if 'summary' in st.session_state:
    st.markdown("### 📑 Summary")
    st.write(st.session_state.summary)

if 'mcqs' in st.session_state:
    st.markdown("### 📝 Quiz Questions")
    st.write(st.session_state.mcqs)

if 'flashcards' in st.session_state:
    st.markdown("### 🎓 Flashcards")
    st.write(st.session_state.flashcards)

if 'explanation' in st.session_state:
    st.markdown("### 📖 AI Explanation")
    st.write(st.session_state.explanation)

# Footer Section
st.markdown("---")
st.markdown("🚀 **ScholarAI | Built by Saumya Mohandas**")
