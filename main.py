import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

# Load Groq API key
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    st.error("❌ GROQ_API_KEY not found in .env file.")
    st.stop()

# Initialize Groq client
client = Groq(api_key=groq_api_key)

# --- Hardcoded Book Passage ---
passage = """
When we strive to become better than we are, everything around us becomes better too.
The boy remembered the crystal merchant. He had once said that he always wanted to
go to Mecca, but he was never able to. He said that he was afraid that, when he had
achieved his dream, he would have no reason to go on living. The boy told himself that
he would never be like the crystal merchant, and that someday he would go back to his
sheep. He knew that it was not love that would keep him from traveling, because he had
already known love, and had left it behind. It had not hurt him then, and it would not
hurt him now.
"""

# --- Streamlit UI ---
st.title("📘 Book Passage Analyzer (Groq Edition)")
st.write("The passage is hardcoded as per assignment instructions.")

with st.expander("📜 View Hardcoded Passage"):
    st.write(passage)

if st.button("Analyze"):
    # --- 1. Word Count ---
    words = passage.split()
    word_count = len(words)
    st.subheader("1️⃣ Total Number of Words")
    st.write(f"**{word_count} words**")

    # --- 2 & 3. Emotion + Summary via Groq LLM ---
    st.subheader("2️⃣ Predominant Emotion")
    st.subheader("3️⃣ Summary (2-3 sentences)")

    prompt = f"""
You are a helpful AI language model.

Analyze the following book passage:
\"\"\"{passage}\"\"\"

Return:
1. The primary emotion conveyed (just the one word: joy, sadness, fear, etc.)
2. A 2-3 sentence summary of the passage.

Respond in this format:
Emotion: <emotion>
Summary: <summary>
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=300
        )

        result = response.choices[0].message.content.strip()

        # Display result
        st.text_area("Result from Groq (Mistral)", result, height=200)

        
        if "Emotion:" in result and "Summary:" in result:
            emotion = result.split("Emotion:")[1].split("Summary:")[0].strip()
            summary = result.split("Summary:")[1].strip()
            st.success(f"**Emotion:** {emotion}")
            st.info(f"**Summary:** {summary}")
    except Exception as e:
        st.error(f"Error from Groq API: {str(e)}")