import streamlit as st
import requests

# Access Groq API key directly from Streamlit Secrets Management
GROQ_API_KEY = st.secrets["groq"]["GROQ_API_KEY"]

# Groq API details
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL_NAME = "llama3-8b-8192"  # or "mixtral-8x7b-32768"

def get_groq_response(prompt, audience, temperature):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    system_instruction = f"You are a blog assistant. Write a blog suitable for {audience.lower()} in a friendly and informative tone."

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": prompt}
        ],
        "temperature": temperature
    }

    response = requests.post(GROQ_API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")

# Streamlit UI
st.set_page_config(page_title="AI Blog Generator", layout="centered")
st.title("📝 AI-Powered Blog Generator")

st.markdown("Generate intelligent, audience-tailored blogs instantly using Groq's LLMs.")

# User Inputs
prompt = st.text_input("📌 Enter your blog topic:")
audience = st.radio("🎯 Who is this content for?", ["Common People", "Students", "Researchers"], horizontal=True)
temperature = st.slider("🎨 Creativity (Temperature)", 0.0, 1.0, 0.7)

# Output area
if st.button("🚀 Generate Blog"):
    if not prompt:
        st.warning("Please enter a topic.")
    else:
        try:
            with st.spinner("Generating your blog..."):
                result = get_groq_response(prompt, audience, temperature)
            st.success("✅ Blog generated successfully!")

            st.subheader("🧠 Generated Blog:")
            edited_blog = st.text_area("✏️ You can edit the blog below:", value=result, height=300)

            st.download_button(
                label="💾 Download Blog",
                data=edited_blog,
                file_name="generated_blog.txt",
                mime="text/plain"
            )
        except Exception as e:
            st.error(f"⚠️ Error: {e}")

# Footer
st.markdown("---")
st.markdown(
    "<center><small>Made with ❤️ using Groq API & Streamlit</small></center>",
    unsafe_allow_html=True
)
