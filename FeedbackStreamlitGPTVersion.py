import streamlit as st
import streamlit.components.v1 as components

# Initialize session state for chat history and feedback
if "messages" not in st.session_state:
    st.session_state.messages = []
if "feedback" not in st.session_state:
    st.session_state.feedback = {}

# Function to handle user input
def handle_input():
    user_input = st.session_state.input_text
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.input_text = ""
        # Simulate a chatbot response
        response = f"Echo: {user_input}"
        st.session_state.messages.append({"role": "assistant", "content": response})

# Function to handle feedback
def handle_feedback(feedback, message_index):
    if message_index > 0 and st.session_state.messages[message_index - 1]["role"] == "user":
        question = st.session_state.messages[message_index - 1]["content"]
        answer = st.session_state.messages[message_index]["content"]
        st.session_state.feedback[message_index] = {
            "feedback": feedback,
            "question": question,
            "answer": answer
        }

# Display chat messages
for index, message in enumerate(st.session_state.messages):
    if message["role"] == "user":
        st.write(f"You: {message['content']}")
    else:
        st.write(f"Assistant: {message['content']}")
        # Add feedback buttons with custom icons next to each other
        col1, col2 = st.columns(2)
        with col1:
            like_button = st.button("👍 Like", key=f"like_{index}", disabled=index in st.session_state.feedback)
        with col2:
            dislike_button = st.button("👎 Dislike", key=f"dislike_{index}", disabled=index in st.session_state.feedback)
        if like_button:
            handle_feedback("like", index)
        if dislike_button:
            handle_feedback("dislike", index)

# Input text box
st.text_input("You:", key="input_text", on_change=handle_input)

# Display feedback summary
st.write("Feedback Summary:")
st.write(list(st.session_state.feedback.values()))
