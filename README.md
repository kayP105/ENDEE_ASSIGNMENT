# Endee Knowledge Assistant  
### Semantic Search and Retrieval-Augmented Generation (RAG) using Endee Vector Database

---

## Project Overview

This project demonstrates how to build a **retrieval-first AI system** using **Endee**, a high-performance vector database, as the **central semantic engine**.

The system supports two closely related but conceptually distinct capabilities:

- **Semantic Search** – retrieving the most relevant document passages using vector similarity  
- **Retrieval-Augmented Generation (RAG)** – generating grounded answers by combining retrieval with a language model  

A key design principle of this project is that **the language model is used only after Endee has selected the most relevant information**. Endee determines *what knowledge is relevant*; the language model is responsible only for *explaining that knowledge*.

---

## What is Endee?

**Endee** is a **high-performance, open-source vector database** designed specifically for **semantic similarity search at scale**.

Unlike traditional databases that store and query structured data (rows, columns, exact matches), Endee is optimized to:

- store high-dimensional vector embeddings  
- perform approximate nearest-neighbor (ANN) search  
- retrieve semantically similar data efficiently  

In modern AI systems, Endee acts as the **semantic memory layer**, enabling applications such as:

- semantic search  
- document retrieval  
- recommendation systems  
- retrieval-augmented generation (RAG)  
- agentic AI workflows  

In this project, Endee serves as the **single source of semantic truth**.

---

## What is a Vector Database?

A **vector database** is a specialized database built to store and query **vector embeddings** — numerical representations of unstructured data such as text, documents, images, audio, or code.

Embedding models convert data into vectors such that:

- semantically similar content produces vectors that are close together  
- semantically different content produces vectors that are far apart  

Vector databases answer questions like:

> Which pieces of data are most similar in meaning to this query?

This capability is fundamental to modern AI systems such as semantic search and RAG.

---

## How Endee Works (High Level)

1. Documents are converted into vector embeddings using an embedding model  
2. These embeddings are stored inside an Endee vector index  
3. When a query arrives:
   - the query is embedded  
   - Endee performs ANN-based similarity search  
4. Endee returns:
   - top-K most relevant results  
   - similarity scores  
   - associated metadata (source file, page number, etc.)

This enables fast, scalable, and explainable semantic retrieval, even for large document collections.

---

## System Architecture

The system is organized into clearly separated layers, each with a single responsibility.

```
User Interface (Streamlit)
├── Accepts user queries
├── Allows mode selection (Semantic Search / RAG)
└── Displays retrieved context and answers
    │
    ↓
Application Layer (Python Backend)
├── Orchestrates the end-to-end pipeline
├── Manages the Endee client
└── Handles ingestion, retrieval, and RAG logic
    │
    ↓
Semantic Layer (Embedding Model)
└── Converts text into vector embeddings
    │
    ↓
Vector Database (Endee)
├── Stores vector embeddings
├── Performs vector similarity search
└── Returns ranked results with metadata
    │
    ↓
Generation Layer (RAG only)
└── Local LLM (Ollama)
    └── Generates grounded answers using retrieved context
```

---

## Semantic Search Architecture

**Purpose:**  
Retrieve relevant document passages based on semantic similarity, without any text generation.

### Pipeline

```
User Query
  → Embedding Model
  → Query Vector
  → Endee Vector Database
  → Top-K Similar Vectors
  → Original Text + Metadata + Confidence
```

### Characteristics

- Retrieval-only (no language model involved)
- Fast response time
- No hallucination
- Fully traceable to source documents

All relevance decisions are made entirely by **Endee**.

---

## Retrieval-Augmented Generation (RAG) Architecture

**Purpose:**  
Generate a grounded explanation using document content retrieved from Endee.

### Pipeline

```
User Question
  → Embedding Model
  → Query Vector
  → Endee Vector Database
  → Top-K Relevant Chunks
  → Prompt Construction
  → Local LLM (Ollama)
  → Final Answer + Citations + Confidence
```

### Key Constraint

The language model receives **only content retrieved by Endee** and never accesses raw documents directly.  
This ensures grounded answers and significantly reduces hallucination.

---

## Document Ingestion Pipeline

Documents are processed before querying and stored semantically inside Endee.

### Pipeline

```
PDF / TXT Document
  → Text Extraction
  → Page-Aware Chunking (with overlap)
  → Deduplication
  → Embedding Generation
  → Endee Vector Index
```

Each stored chunk includes metadata such as:
- source file
- page number
- original text

This enables traceability, citations, and explainable retrieval.

---

## Project Setup and Installation

### 1. Setting Up Endee (Vector Database)

Endee is run as a **standalone service using Docker**, based on the official Endee repository image.  
The internal C++ code of Endee is not modified.

#### 1.1 Docker Compose Configuration

Create a `docker-compose.yml` file:

```yaml
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
```

This configuration:

- runs Endee on localhost:8080
- persists vector data using Docker volumes
- runs without authentication for local development

#### 1.2 Start Endee

```bash
docker-compose up -d
```

Verify Endee is running:

```bash
curl http://localhost:8080/api/v1/index/list
```

Expected output:

```json
{"indexes":[]}
```

### 2. Installing the Endee Python SDK

The application communicates with Endee using its official Python SDK.

```bash
pip install endee
```

The SDK provides:

- index creation and management
- vector upsert and query operations
- a clean abstraction over Endee's REST API

### 3. Endee Client Configuration

The backend initializes a connection to Endee using a dedicated client wrapper.

**backend/endee_client.py**

```python
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
```

This logic ensures:

- idempotent index creation
- safe recovery after container restarts
- no manual index management

### 4. Installing Application Dependencies

All Python dependencies are listed in requirements.txt.

```bash
pip install -r requirements.txt
```

Key dependencies include:

- sentence-transformers (embeddings)
- streamlit (UI)
- pypdf (PDF parsing)
- requests (networking)
- endee (vector database SDK)

### 5. Installing and Running Ollama (Local LLM)

Ollama is used to run a local language model for the RAG pipeline.

Download Ollama from:

https://ollama.com

Start the Ollama service:

```bash
ollama serve
```

Pull a lightweight model:

```bash
ollama pull mistral
```

This model is chosen for fast CPU inference and suitability for local demo environments.

### 6. Running the Application

Once Endee and Ollama are running, start the application:

```bash
streamlit run app.py
```

The UI will be available at:

http://localhost:8501

---

## Execution Order Summary

1. Start Endee using Docker
2. Verify Endee is reachable
3. Install Python dependencies
4. Start Ollama
5. Run the Streamlit application

**Endee must always be running before the application starts.**

---

## Key Design Choice

Endee is intentionally deployed as a separate service rather than embedded into the application. This mirrors real-world production systems where:

- vector databases run independently
- application services scale separately
- retrieval remains reliable across restarts
