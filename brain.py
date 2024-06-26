import re
from io import BytesIO
from typing import Tuple, List
from sentence_transformers import SentenceTransformer
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pypdf import PdfReader
import pinecone
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

if not PINECONE_API_KEY or not PINECONE_ENVIRONMENT:
    raise ValueError("Pinecone API key or environment not found. Please add them to the .env file.")

if not HUGGINGFACE_API_KEY:
    raise ValueError("Hugging Face API key not found. Please add it to the .env file.")

# Initialize Pinecone
pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENVIRONMENT)

# Create a Pinecone index if it doesn't exist
index_name = "pdf-embeddings"
if index_name not in pinecone.list_indexes():
    pinecone.create_index(index_name, dimension=384)  # Dimension should match the embedding size

# Connect to the index
index = pinecone.Index(index_name)

def parse_pdf(file: BytesIO, filename: str) -> Tuple[List[str], str]:
    pdf = PdfReader(file)
    output = []
    for page in pdf.pages:
        text = page.extract_text()
        text = re.sub(r"(\w+)-\n(\w+)", r"\1\2", text)
        text = re.sub(r"(?<!\n\s)\n(?!\s\n)", " ", text.strip())
        text = re.sub(r"\n\s*\n", "\n\n", text)
        output.append(text)
    return output, filename

def text_to_docs(text: List[str], filename: str) -> List[Document]:
    if isinstance(text, str):
        text = [text]
    page_docs = [Document(page_content=page) for page in text]
    for i, doc in enumerate(page_docs):
        doc.metadata["page"] = i + 1

    doc_chunks = []
    for doc in page_docs:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=4000,
            separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""],
            chunk_overlap=0,
        )
        chunks = text_splitter.split_text(doc.page_content)
        for i, chunk in enumerate(chunks):
            doc_chunk = Document(
                page_content=chunk, metadata={"page": doc.metadata["page"], "chunk": i}
            )
            doc_chunk.metadata["source"] = f"{doc.metadata['page']}-{doc.metadata['chunk']}"
            doc_chunk.metadata["filename"] = filename  # Add filename to metadata
            doc_chunks.append(doc_chunk)
    return doc_chunks

def docs_to_index(docs):
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2', use_auth_token=HUGGINGFACE_API_KEY)
    embeddings = model.encode([doc.page_content for doc in docs])
    
    # Upsert embeddings to Pinecone
    vectors = [(str(i), embeddings[i].tolist(), doc.metadata) for i, doc in enumerate(docs)]
    index.upsert(vectors)
    
    return index

def get_index_for_pdf(pdf_files, pdf_names):
    documents = []
    for pdf_file, pdf_name in zip(pdf_files, pdf_names):
        text, filename = parse_pdf(BytesIO(pdf_file), pdf_name)
        documents += text_to_docs(text, filename)
    index = docs_to_index(documents)
    return index
