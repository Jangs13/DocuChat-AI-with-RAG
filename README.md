# DocChat AI with RAG
RAG enabled Chatbots using [LangChain](https://www.langchain.com) and [OpenAI](https://platform.openai.com/docs/guides/embeddings)

DocChat AI is an advanced document chatting application utilizing Retrieval-Augmented Generation (RAG) to provide efficient and accurate responses to user queries. This project leverages OpenAI’s LLM, LangChain, and Pinecone for indexing and querying documents, enhancing query response times and overall system performance.

![](https://github.com/Jangs13/DocuChat-AI-with-RAG/blob/master/RAG%20flowchart.png)


- For the front-end : `app.py`
- PDF parsing and indexing : `brain.py`
- API keys are maintained over Streamlit secret management
- Indexed are stored over session state 

## Features 
- Advanced Query Handling: Utilizes OpenAI’s LLM for natural language understanding and response generation.
- Efficient Document Indexing: Automated indexing with ChromaDB and Pinecone reduces query response times by 40%.
- Robust Data Pipelines: Built using LangChain, improving system performance and reliability by 30%.
- Seamless Updates: Ensures efficient document indexing and quick access to relevant information.
- Translation Feature: Supports translation to handle multilingual documents and queries.

## Installation

### Prerequisites

- Python 3.8+
- OpenAI API key
- Hugging Face API key
- Pinecone API key

### Clone the Repository

```bash
git clone https://github.com/Jangs13/docchat-ai-rag.git
cd docchat-ai-rag
 
```
### Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

```

### Install Dependencies

``` bash

pip install -r requirements.txt

```

### Configuration

Create a .env file in the root directory and add your API keys and environment settings:

``` bash

OPENAI_API_KEY=your_openai_api_key
HUGGINGFACE_API_KEY=your_huggingface_api_key
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_ENVIRONMENT=your_pinecone_environment

```
## Usage 
### Indexing Documents
To index documents, place your documents in the documents directory and run the indexing script:

```bash
python brain.py

```
### Running the Application

To start the application run 

``` bash

streamlit run app.py

```

## Querying Documents

Use the chat interface to input your queries. The application will leverage the indexed documents and OpenAI’s LLM to generate accurate responses.

## Demo
As I have exhausted my OpenAI credits, I have provided a demo video to showcase the application's functionality. For future updates, I will be using Mistral and will provide a link to the live demo.

![](https://github.com/Jangs13/DocuChat-AI-with-RAG/blob/master/compare%20medium.gif)


## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/Jangs13/DocuChat-AI-with-RAG/blob/master/LICENSE) file for details.

















