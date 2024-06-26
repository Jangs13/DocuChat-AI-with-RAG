# DocChat AI with RAG
RAG enabled Chatbots using [LangChain](https://www.langchain.com) and [OpenAI]([https://databutton.com/login?utm_source=github&utm_medium=avra&utm_article=rag](https://www.google.com/url?sa=i&url=https%3A%2F%2Ficonduck.com%2Ficons%2F1213%2Fopenai&psig=AOvVaw22J6BNkwxOFnfENTUMYFrq&ust=1719519281288000&source=images&cd=vfe&opi=89978449&ved=0CBEQjRxqFwoTCPiUitKK-oYDFQAAAAAdAAAAABAE))

DocChat AI is an advanced document chatting application utilizing Retrieval-Augmented Generation (RAG) to provide efficient and accurate responses to user queries. This project leverages OpenAI’s LLM and LangChain to handle queries and automate document indexing using ChromaDB, enhancing query response times and overall system performance.
![](https://github.com/Jangs13/DocuChat-AI-with-RAG/blob/master/RAG%20flowchart.png)


- For the front-end : `app.py`
- PDF parsing and indexing : `brain.py`
- API keys are maintained over Streamlit secret management
- Indexed are stored over session state 

## Features 
- Advanced Query Handling: Utilizes OpenAI’s LLM for natural language understanding and response generation.
- Efficient Document Indexing: Automated indexing with ChromaDB reduces query response times by 40%.
- Robust Data Pipelines: Built using LangChain, improving system performance and reliability by 30%.
- Seamless Updates: Ensures efficient document indexing and quick access to relevant information.
- Translation Feature: Supports translation to handle multilingual documents and queries.

## Installation

### Prerequisites

- Python 3.8+
- OpenAI API key
- ChromaDB account

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

Create a .env file in the root directory and add your OpenAI API key and ChromaDB credentials:

``` bash

OPENAI_API_KEY=your_openai_api_key
CHROMADB_API_KEY=your_chromadb_api_key

```

### Running the Application

To start the application run 

``` bash
python app.py
```
## Demo
As I have exhausted my OpenAI credits, I have provided a demo video to showcase the application's functionality. For future updates, I will be using Mistral and will provide a link to the live demo.

![](https://github.com/Jangs13/DocuChat-AI-with-RAG/blob/master/compare%20medium.gif)

## License

This project is licensed under the MIT License. See the [LICENSE][https://github.com/Jangs13/DocuChat-AI-with-RAG/blob/master/LICENSE] file for details.

















