import os
import time
import openai
import streamlit as st
from openai import OpenAIError

# Load API key
my_api_key = os.environ.get("OPENAI_API_KEY")

# Hardcoded Assistant and File IDs
FILE_ID = "file-NorprFaMGtH5YSz5oF1XsC"
ASSISTANT_ID = "asst_zacZD9hFPv4iyyVLJDLWXb3l"

openai_session = openai.OpenAI(api_key=my_api_key)

# Function to check if the assistant exists
def check_assistant_exists():
    try:
        assistant = openai_session.beta.assistants.retrieve(assistant_id=ASSISTANT_ID)
        return assistant
    except OpenAIError:
        return None

# Function to check if the manual is uploaded
def check_manual_uploaded():
    try:
        file = openai_session.files.retrieve(FILE_ID)
        return file
    except OpenAIError as e:
        print(f"Error occurred while retrieving file: {e}")
        return None

def ask_gpt(question, thread_id=None):
    if thread_id is None:
        thread = openai_session.beta.threads.create()
        thread_id = thread.id

    print("Sending message to GPT...")

    attachments = [{
        'file_id': FILE_ID,
        'tools': [{'type': 'file_search'}]
    }]

    openai_session.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=question,
        attachments=attachments
    )

    run = openai_session.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=ASSISTANT_ID
    )

    print("Waiting for GPT response...")
    while True:
        status = openai_session.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
        if status.status == "completed":
            break
        time.sleep(1)

    # Retrieve and display the assistant's last response
    messages = openai_session.beta.threads.messages.list(thread_id=thread_id)
    assistant_response = "The wind speaks not today, my friend."  # default response in case no assistant response is found

    for message in messages.data:
        if message.role == "assistant":
            assistant_response = message.content[0].text.value
            # print(f"\nAssistant: {assistant_response}")
            break

    return assistant_response, thread_id



# Streamlit UI
st.title("🏯 Samurai Mechanic 🚗")
st.write("Ask your question, and the samurai will share wisdom from the sacred scrolls of your 3000GT car manual.")

assistant = check_assistant_exists()
manual_file = check_manual_uploaded()

if not assistant:
    st.error("The samurai has not yet been summoned. Assistant ID is invalid.")
elif not manual_file:
    st.error("The sacred scroll is missing. File ID is invalid.")
else:
    # Initialize thread state if needed
    if "thread_id" not in st.session_state:
        st.session_state.thread_id = None

    user_question = st.text_input("Enter your question:")

    if st.button("Ask the Samurai"):
        if user_question:
            response, thread_id = ask_gpt(user_question, thread_id=st.session_state.thread_id)
            st.session_state.thread_id = thread_id
            st.write(f"**The Samurai responds:**\n{response}")
        else:
            st.warning("Please enter a question to ask the Samurai.")

    if st.session_state.thread_id:
        if st.button("End Session"):
            try:
                # Delete the thread
                openai_session.beta.threads.delete(thread_id=st.session_state.thread_id)
                
                # Verify that the thread has been deleted
                try:
                    # Try to retrieve the thread, if it raises an error, it means the thread is deleted
                    openai_session.beta.threads.retrieve(thread_id=st.session_state.thread_id)
                    st.warning("The thread still exists. Deletion failed.")
                except OpenAIError:
                    st.success("The samurai bows and the scroll is returned to its shrine. The thread has been successfully deleted.")
                    st.session_state.thread_id = None
            except Exception as e:
                st.error(f"An error occurred while deleting the thread: {e}")


