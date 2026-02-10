Endee Knowledge assistant
Topic: Semantic Search and retreival Augemnted Generation(RAG) using Endee Vector Datatbase
-------------------------------------------------------------------------------------------------------------------------
Using Endee (high performance vector database) as the central component ,the system supports two very close but distinct capabilities -

   *Semantic Search-retrieving the most relevant document passages using vector similarity
   
   *Retrieval-Augmented Generation (RAG) – generating grounded answers by combining retrieval with a language model
   
The language model is used only after Endee has selected the most relevant information.
_________________________________________________________________________________________________________________________
Endee
------
Endee is a high-performance open-source vector database designed specifically for semantic similarity search at scale.

Unlike traditional databases that store and query structured data (rows, columns, exact matches), Endee is optimized to store high-dimensional vectors and efficiently retrieve the most semantically similar vectors using approximate nearest-neighbor (ANN) search.

In modern AI systems, Endee serves as the semantic memory layer — enabling applications such as:

*semantic search

*document retrieval

*recommendation systems

*Retrieval-Augmented Generation (RAG)

*agentic AI workflows

What is a Vector Database?

A vector database is a specialized database built to store and query vector embeddings — numerical representations of data such as text, images, audio, or code.

How Endee Works Internally (High Level)

Data (text, documents, etc.) is converted into embeddings using an embedding model

These embeddings are stored in Endee’s vector index

When a query arrives:

the query is embedded

Endee finds the nearest vectors using efficient ANN algorithms

Endee returns the most relevant results along with similarity scores and metadata

This process enables fast, scalable semantic retrieval, even with large datasets.

User Query                                                     User Question          
   ↓                                                                 ↓ 
Text Embedding Model                                           Text Embedding Model
   ↓                                                                  ↓
Query Vector                                                   Query Vector
   ↓                                                                  ↓    
Endee Vector Database                                            Endee Vector Database
   ↓                                                               ↓
Top-K Similar Vectors                                            Top-K Relevant Chunks
   ↓                                                                   ↓
Original Text + Metadata                                                Prompt Construction    
                                                                           ↓
                                                                 Local LLM (Ollama)
                                                                         ↓
                                                              Final Answer + Citations


┌─────────────────────┐

│  User Interface     │

│  (Streamlit)        │

└─────────┬───────────┘

          ↓
          
┌─────────────────────┐

│  Application Layer  │

│  (Python Backend)   │

└─────────┬───────────┘

          ↓
          
┌─────────────────────┐
│  Semantic Layer     │
│  (Embeddings)       │
└─────────┬───────────┘
          ↓
┌─────────────────────┐
│  Vector Database    │
│  (Endee)            │
└─────────────────────┘
          ↓
┌─────────────────────┐
│  Generation Layer   │
│  (Local LLM – RAG)  │
└─────────────────────┘

Why This Architecture Works Well
1. Separation of Concerns

Retrieval ≠ Generation

Each component has one clear responsibility

2. Endee-Centric Design

Endee determines what knowledge is relevant

LLM only explains retrieved knowledge

3. Scalability

Vector search scales independently

LLM can be swapped without changing retrieval

4. Explainability

Every answer can be traced back to documents

Page-level citations are preserved



1.1 Using the Endee Repository via Docker

The official Endee repository provides a Docker-based setup, which is the recommended way to run Endee locally.

This project uses Endee as a standalone vector database service, without modifying its internal C++ code.

1.2 Docker Compose Configuration

A minimal docker-compose.yml is used to run Endee and persist vector data.

services:
  endee:
    image: endeeio/endee-server:latest
    container_name: endee-server
    ports:
      - "8080:8080"
    environment:
      NDD_AUTH_TOKEN: ""
    volumes:
      - endee-data:/data
    restart: unless-stopped

volumes:
  endee-data:


This setup:

runs Endee on localhost:8080

persists index data using Docker volumes

runs without authentication for local development

1.3 Start Endee
docker-compose up -d


Verify Endee is running:

curl http://localhost:8080/api/v1/index/list


Expected output:

{"indexes":[]}

2️⃣ Installing the Endee Python SDK

The application communicates with Endee using its official Python SDK.

pip install endee


This SDK provides:

index creation and management

vector upsert and query operations

a clean abstraction over Endee’s REST API

3️⃣ Application Configuration (Endee Client)

The backend initializes a connection to Endee using a dedicated client wrapper.

backend/endee_client.py
from endee import Endee, Precision
from endee.exceptions import ConflictException, NotFoundException
from backend.config import INDEX_NAME, EMBEDDING_DIM

ENDEE_URL = "http://localhost:8080"

def get_index():
    client = Endee(base_url=ENDEE_URL)

    try:
        client.create_index(
            name=INDEX_NAME,
            dimension=EMBEDDING_DIM,
            space_type="cosine",
            precision=Precision.INT8D
        )
    except ConflictException:
        pass

    try:
        return client.get_index(INDEX_NAME)
    except NotFoundException:
        client.delete_index(INDEX_NAME)
        client.create_index(
            name=INDEX_NAME,
            dimension=EMBEDDING_DIM,
            space_type="cosine",
            precision=Precision.INT8D
        )
        return client.get_index(INDEX_NAME)


This logic ensures:

idempotent index creation

safe recovery after container restarts

no manual intervention required

4️⃣ Installing Application Dependencies

All Python dependencies are listed in requirements.txt.

pip install -r requirements.txt


Key dependencies include:

sentence-transformers (embeddings)

streamlit (UI)

pypdf (PDF parsing)

requests (networking)

endee (vector DB SDK)

5️⃣ Installing and Running Ollama (Local LLM)

Ollama is used to run a local language model for the RAG pipeline.

5.1 Install Ollama

Download from:

https://ollama.com

5.2 Start Ollama Service
ollama serve

5.3 Pull a Model
ollama pull mistral


This model is chosen for:

fast CPU inference

low memory usage

suitability for demo environments

6️⃣ Running the Application

Once Endee and Ollama are running, start the application:

streamlit run app.py


The UI will be available at:

http://localhost:8501

7️⃣ Execution Order Summary

The correct startup sequence is:

Start Endee (Docker)

Verify Endee is reachable

Install Python dependencies

Start Ollama

Run the Streamlit application

Endee must always be running before the application starts.

🔑 Key Design Choice

Endee is intentionally started as a separate service rather than embedded into the application.

This mirrors real-world deployments where:

vector databases run independently

application services scale separately

retrieval remains reliable even if the UI restarts
