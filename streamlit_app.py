import os
from dotenv import load_dotenv
from openai import OpenAI
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
# Load API key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))




# Initialize chat history in Streamlit session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a professional SAT prep tutor helping students improve their skills in Math, Reading, and Writing. Always provide helpful explanations, test strategies, and practice-style responses. Break down complex questions clearly and offer tips for mastering the SAT."}
    ]

st.title("📚 SAT Prep Tutor")
st.write("Boost your SAT score with AI tutoring! Ask questions from Math, Reading, or Writing. You can also get test strategies.")

if "subject" not in st.session_state:
    st.session_state.subject = "Math"


subject = st.selectbox(
    "📚 Select SAT Subject Area:",
    ["Math", "Reading", "Writing"],
    index=["Math", "Reading", "Writing"].index(st.session_state.subject)
)

if subject != st.session_state.subject:
    st.session_state.subject = subject
    st.session_state.messages = [
        {"role": "system", "content": f"You are a helpful SAT tutor specializing in {subject}. Always explain concepts clearly, provide examples, and help the student learn."}
    ]
    st.rerun()


# Input box
question = st.chat_input("Ask your SAT question:")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Reset button
if st.button("🔄 Reset Conversation"):
    st.session_state.messages = [
        {"role": "system", "content": f"You are a helpful SAT tutor specializing in {subject}. Always explain concepts clearly, provide examples, and help the student learn."}
    ]
    st.rerun()

# On question submit
if question:
    st.session_state.messages.append({"role": "user", "content": question})

    response = client.chat.completions.create(
        model="gpt-4",
        messages=st.session_state.messages
    )

    answer = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": answer})


# Display conversation
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"**Student:** {msg['content']}")
    elif msg["role"] == "assistant":
        st.markdown(f"**Tutor:** {msg['content']}")
