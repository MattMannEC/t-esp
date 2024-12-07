# RAG system

### Docker services

This Docker stack hosts a RAG (Retrieval-Augmented Generation) system with multiple interconnected services:

1. **ChromaDB**  
   - **Purpose:** Manages the vector store to store and retrieve document embeddings efficiently.  
   - **Image:** `chromadb/chroma:latest`  
   - **Configuration:**  
     - Persistent storage enabled via `IS_PERSISTENT=TRUE`.  
     - Stores embeddings in a directory mapped to the volume `chromadb`.  
     - Exposes its service on port `8000`.  

2. **Redis**  
   - **Purpose:** Acts as a lightweight in-memory database for handling fast messaging or temporary data storage (e.g., streaming responses).  
   - **Image:** `redis:latest`  
   - **Configuration:** Exposes the default Redis port `6379`.

3. **API**  
   - **Purpose:** Orchestrates the RAG workflow by interacting with other services (ChromaDB for embeddings, Redis for streaming, and Ollama for LLM inference).  
   - **Configuration:**  
     - Built from a custom Dockerfile (`Dockerfile.api`).  
     - Depends on ChromaDB and Redis for its functionality.  
     - Communicates with the Ollama service via the environment variable `OLLAMA_SERVER_URL`.  
     - Maps local volumes for Hugging Face models and application files.  
     - Exposes its API on port `8001`.  

4. **Ollama**  
   - **Purpose:** Hosts the LLM used for generating answers to user queries.  
   - **Image:** `ollama/ollama`.  
   - **Configuration:**  
     - Stores its data in the volume `ollama`.  
     - Exposes its service on port `11434`.  

5. **Volumes**  
   - `chromadb`: Persistent storage for ChromaDB embeddings.  
   - `ollama`: Persistent storage for Ollama's model data.  
   - `huggingface`: Cache for Hugging Face models used by the API service.  


### Overview of Functionality:
- User queries are sent to the **API** service.  
- The **API** retrieves relevant documents from **ChromaDB** (vector store).  
- Redis is used for handling real-time streaming responses.  
- The **API** sends the query and retrieved context to **Ollama** (LLM) to generate a response.  
- All components communicate seamlessly via Docker's networking and exposed ports.

Here's an improved version of your README with better structure, clarity, and formatting:

---

### Getting Started

#### Prerequisites

Ensure you have the following installed and configured on your system:  

1. **Linux Distribution or WSL (Windows Subsystem for Linux)**  
   Recommended for native compatibility.  

2. **Docker and Docker Compose**  
   To manage containers for the system.  

3. **Python 3.12 Environment**  
   Set up with a tool like [Pyenv](https://github.com/pyenv/pyenv) for managing Python versions.  

---

#### Setup Instructions  

Follow these steps to get the system up and running:  

##### 1. Configure Environment Variables  
Rename `.env.example` to `.env` and update it with your specific configurations if needed.  

##### 2. Start Database Container  
Run the following command to start the Docker containers:  
```bash
docker compose up
```  

##### 3. Pull the Language Model (LLM)  
Launch the Ollama container and pull the desired LLM:  
```bash
ollama pull MODEL_NAME
```  

##### 4. Load Documents into the Vector Store  
Use the `rag.ipynb` Jupyter Notebook to load your documents into the vector store.  
- Make sure you have a PDF document to process.  
- Configure the file path by updating the `file_path` variable in the notebook.  

##### 5. Run the RAG System  
- Tokens are streamed via Server-Sent Events (SSE) over a Redis instance.  
- To test the system:  
  1. Create an EventSource instance pointing to `http://localhost:8001/stream`. Refer to the [MDN Server-Sent Events guide](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events) for more details.  
  2. Send a POST request to `http://localhost:8001/simulate_llm` with parameters:  
     ```json
     {
       "prompt": "Your prompt here"
     }
     ```  

---

### Demo Chat Interface  

You can run a demo chat interface using the provided Vue app:  

1. Navigate to the `chatbot` directory:  
   ```bash
   cd chatbot
   ```  

2. Install dependencies and start the development server:  
   ```bash
   npm install && npm run dev
   ```  

The chat interface will be available on your local server.

--- 



