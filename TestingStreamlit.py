import streamlit as st
import pandas as pd
from datetime import datetime

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = pd.DataFrame(columns=['timestamp', 'question', 'answer', 'feedback'])

def save_conversation(question, answer, feedback=None):
    """Save a conversation pair with optional feedback"""
    new_row = pd.DataFrame([{
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'question': question,
        'answer': answer,
        'feedback': feedback
    }])
    st.session_state.chat_history = pd.concat([st.session_state.chat_history, new_row], ignore_index=True)
    # Save to CSV after each update
    st.session_state.chat_history.to_csv('chat_history.csv', index=False)

def handle_input():
    user_input = st.session_state.user_input
    if user_input:
        # Simulate bot response - replace with your actual bot logic
        bot_response = f"Echo: {user_input}"
        
        # Save conversation without feedback initially
        save_conversation(user_input, bot_response)
        
        # Clear input
        st.session_state.user_input = ""

def handle_feedback(idx, feedback_type):
    # Update feedback for the conversation
    st.session_state.chat_history.at[idx, 'feedback'] = feedback_type
    # Save updated data to CSV
    st.session_state.chat_history.to_csv('chat_history.csv', index=False)

# Chat UI
st.title("Chat with Feedback")

# Display messages and feedback buttons
for idx, row in st.session_state.chat_history.iterrows():
    # Display the conversation
    st.write(f"You: {row['question']}")
    st.write(f"Assistant: {row['answer']}")
    
    # Create two columns for the buttons
    col1, col2 = st.columns([1, 1])
    
    # Only show enabled buttons if no feedback yet
    with col1:
        if st.button("👍", key=f"like_{idx}", 
                    disabled=pd.notna(row['feedback']),
                    type="primary" if row['feedback'] == 'like' else "secondary"):
            handle_feedback(idx, "like")
            
    with col2:
        if st.button("👎", key=f"dislike_{idx}", 
                    disabled=pd.notna(row['feedback']),
                    type="primary" if row['feedback'] == 'dislike' else "secondary"):
            handle_feedback(idx, "dislike")

# Input box
st.text_input("Type your message:", key="user_input", on_change=handle_input)

# Show data and download button
if st.checkbox("Show conversation history"):
    st.dataframe(st.session_state.chat_history)

if st.button("Download Chat History"):
    st.download_button(
        label="Download History CSV",
        data=st.session_state.chat_history.to_csv(index=False),
        file_name="chat_history.csv",
        mime="text/csv"
    )