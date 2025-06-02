import streamlit as st
import requests 
import os 
from dotenv import load_dotenv


#Load Api key
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama3-8b-8192"

#page setup
st.set_page_config(page_title="Multingual Chat Bot", layout="centered")


#sidebar
with st.sidebar:
    st.title("Medical Bot")
    selected_mode = st.selectbox("Choose a task", [
        "Symptom Checker",
        "Health Advice",
        "Appointment Scheduling",
        "Medical Q&A",
        "Medication Reminders"
    ])
    st.markdown("""
     How I can help you:
    - Symptom checking  
    - Health advice  
    - Appointment booking  
    - Medical Q&A  
    - Reminders setup  
    """)

    if "messages" not in st.session_state:
        system_prompt = "You are a helpful medical assistant. Keep your responses short, clear, and no longer than 3-4 sentences."


        if "Symptom" in selected_mode:
            system_prompt +=  " Help the user identify possible conditions based on their symptoms."

        elif "Health Advice" in selected_mode:
            system_prompt +=  " Give healthy lifestyle and wellness advice tailored to the user's questions."
        elif "Appointment" in selected_mode:
            system_prompt += " Help the user book a doctor appointment by asking about symptoms, preferred date/time, and doctor preferences."
        elif "Medical Q&A" in selected_mode:
            system_prompt += " Answer general medical questions in a clear and accurate way."
        elif "Medication Reminders" in selected_mode:
            system_prompt += " Help the user set medication reminders based on name, dosage, and timing."


        st.session_state.messages=[{"role": "system", "content": system_prompt}]
    

st.markdown("<h1 style='text-align:center;'>AI Medical ChatBot Assistant</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Talk to your assistant for medical help, advice, or reminders.</p><hr>", unsafe_allow_html=True)


#user input
user_input = st.chat_input("Type your message here...")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})


    response = requests.post(
         "https://api.groq.com/openai/v1/chat/completions",
         headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
         }, 
            json={
            "model": GROQ_MODEL,
            "messages": st.session_state.messages,
            "temperature": 0.6
        }
    )

    #Handle API response
    if response.status_code == 200:
        bot_reply = response.json()["choices"][0]["message"]["content"]

    else:
        bot_reply = "Error connecting to Groq API."
    

    st.session_state.messages.append({"role": "assistant", "content": bot_reply})


# Display messages (avoid duplication)
for msg in st.session_state.messages[1:]:  # Skip system prompt
    if msg["role"] == "user":
        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(
                f"""
                <div style='
                    background-color: #D0EBFF;
                    color: #003366;
                    padding: 12px;
                    border-radius: 12px;
                    margin-bottom: 10px;
                    box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
                '>{msg['content']}</div>
                """,
                unsafe_allow_html=True
            )
    elif msg["role"] == "assistant":
        with st.chat_message("assistant", avatar="💬"):
            st.markdown(
                f"""
                <div style='
                    background-color: #F1F3F5;
                    color: #212529;
                    padding: 12px;
                    border-radius: 12px;
                    margin-bottom: 10px;
                    border-left: 5px solid #4CAF50;
                    box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
                '>{msg['content']}</div>
                """,
                unsafe_allow_html=True
            )

