import os
from dotenv import load_dotenv
from openai import OpenAI
from datetime import datetime

# Load API key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Start a new chat history
def init_chat_history():
    return [
        {"role": "system", "content": "You are a helpful AI tutor. Guide the student step by step, ask questions, and help them learn."}
    ]

# Initialize global history
chat_history = init_chat_history()

def ask_tutor(question):
    chat_history.append({"role": "user", "content": question})

    response = client.chat.completions.create(
        model="gpt-4",
        messages=chat_history
    )

    reply = response.choices[0].message.content
    chat_history.append({"role": "assistant", "content": reply})
    return reply

def save_conversation(history):
    # Remove system prompt for cleaner output
    filtered = [m for m in history if m['role'] != 'system']

    # Create filename
    now = datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename = f"logs/session_{now}.txt"

    # Write each exchange to file
    with open(filename, 'w', encoding='utf-8') as f:
        for msg in filtered:
            role = "Student" if msg['role'] == 'user' else "Tutor"
            f.write(f"{role}: {msg['content']}\n\n")

    print(f"📁 Conversation saved to {filename}")

if __name__ == "__main__":
    print("Welcome to your AI tutor! Type 'reset' to start a new topic, or 'exit' to quit.")

    while True:
        user_q = input("Ask your question: ").strip()

        if user_q.lower() == "exit":
            save_conversation(chat_history)
            print("Goodbye! 👋")
            break

        elif user_q.lower() == "reset":
            chat_history = init_chat_history()
            print("🔄 Tutor has reset. Start your new topic!\n")
            continue

        reply = ask_tutor(user_q)
        print("\nTutor:", reply, "\n")



