import streamlit as st
from brain import get_index_for_pdf
import os
from dotenv import load_dotenv
from transformers import pipeline
from sentence_transformers import SentenceTransformer

# Load environment variables from .env file
load_dotenv()

HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

# Set the title for the Streamlit app
st.title("RAG Enhanced Chatbot with Pinecone")

# Initialize Hugging Face text generation pipeline
generator = pipeline('text-generation', model='gpt2', use_auth_token=HUGGINGFACE_API_KEY)

# Cached function to create a vectordb for the provided PDF files
@st.cache_data
def create_vectordb(files, filenames):
    # Show a spinner while creating the vectordb
    with st.spinner("Creating vector database..."):
        vectordb = get_index_for_pdf([file.getvalue() for file in files], filenames)
    return vectordb

# Upload PDF files using Streamlit's file uploader
pdf_files = st.file_uploader("", type="pdf", accept_multiple_files=True)

# If PDF files are uploaded, create the vectordb and store it in the session state
if pdf_files:
    pdf_file_names = [file.name for file in pdf_files]
    st.session_state["vectordb"] = create_vectordb(pdf_files, pdf_file_names)

# Define the template for the chatbot prompt
prompt_template = """
    You are a helpful Assistant who answers users' questions based on multiple contexts given to you.
    Keep your answer short and to the point.
    The evidence is the context of the PDF extract with metadata.
    Carefully focus on the metadata, especially 'filename' and 'page' whenever answering.
    Make sure to add filename and page number at the end of the sentence you are citing to.
    Reply "Not applicable" if the text is irrelevant.
    The PDF content is:
    {pdf_extract}
"""

# Get the current prompt from the session state or set a default value
prompt = st.session_state.get("prompt", [{"role": "system", "content": "none"}])

# Display previous chat messages
for message in prompt:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.write(message["content"])

# Get the user's question using Streamlit's chat input
question = st.chat_input("Ask anything")

# Handle the user's question
if question:
    vectordb = st.session_state.get("vectordb", None)
    if not vectordb:
        with st.message("assistant"):
            st.write("You need to provide a PDF")
            st.stop()

    # Search the vectordb for similar content to the user's question
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2', use_auth_token=HUGGINGFACE_API_KEY)
    query_vector = model.encode(question)
    search_results = vectordb.query(queries=[query_vector], top_k=3, include_metadata=True)

    pdf_extract = "\n".join([result['metadata']['page_content'] for result in search_results['matches']])

    # Update the prompt with the PDF extract
    prompt[0] = {
        "role": "system",
        "content": prompt_template.format(pdf_extract=pdf_extract),
    }

    # Add the user's question to the prompt and display it
    prompt.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)

    # Display an empty assistant message while waiting for the response
    with st.chat_message("assistant"):
        botmsg = st.empty()

    # Generate response using Hugging Face model
    response = generator(prompt_template.format(pdf_extract=pdf_extract) + question, max_length=500)[0]['generated_text']

    # Display the response
    botmsg.write(response)

    # Add the assistant's response to the prompt
    prompt.append({"role": "assistant", "content": response})

    # Store the updated prompt in the session state
    st.session_state["prompt"] = prompt
