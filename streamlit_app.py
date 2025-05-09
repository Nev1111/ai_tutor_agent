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

# Input box
question = st.text_input("Your Question")

# Reset button
if st.button("🔄 Reset Conversation"):
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful AI tutor. Ask guiding questions and help the student learn."}
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
# If user asked for a plot, try extracting and plotting a quadratic expression
if "plot" in question.lower() and "x" in question.lower():
    try:
        # For now, assume form: y = ax^2 + bx + c (basic parser)
        import re
        match = re.search(r'y\s*=\s*([+-]?\d*)x\^2\s*([+-]?\d*)x\s*([+-]?\d+)', question.replace(" ", ""))
        if match:
            a = int(match.group(1) or 1)
            b = int(match.group(2) or 0)
            c = int(match.group(3))

            x_vals = np.linspace(-10, 10, 400)
            y_vals = a * x_vals**2 + b * x_vals + c

            fig, ax = plt.subplots()
            ax.plot(x_vals, y_vals)
            ax.axhline(0, color='gray', lw=1)
            ax.axvline(0, color='gray', lw=1)
            ax.set_title(f"Graph of y = {a}x² + {b}x + {c}")
            st.pyplot(fig)
    except Exception as e:
        st.error(f"Could not generate plot: {e}")

# Display conversation
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"**Student:** {msg['content']}")
    elif msg["role"] == "assistant":
        st.markdown(f"**Tutor:** {msg['content']}")
