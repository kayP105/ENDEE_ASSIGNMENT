Endee Knowledge assistant
Topic: Semantic Search and retreival Augemnted Generation(RAG) using Endee Vector Datatbase
This project demonstrates how to build a retrieval-first AI system using Endee, a high-performance vector database, as the core semantic engine.

The system supports two closely related but conceptually distinct capabilities:

Semantic Search – retrieving the most relevant document passages using vector similarity

Retrieval-Augmented Generation (RAG) – generating grounded answers by combining retrieval with a language model

A key design principle of this project is that the language model is only used after Endee has selected the most relevant information.
Endee is responsible for what knowledge is relevant; the LLM is responsible only for explaining that knowledge.

🧠 What is Endee?

Endee is a high-performance, open-source vector database designed specifically for semantic similarity search at scale.

Unlike traditional databases that operate on structured data (rows, columns, exact matches), Endee is optimized to:

store high-dimensional vector embeddings

perform approximate nearest-neighbor (ANN) search

retrieve semantically similar data efficiently and reliably

In modern AI systems, Endee acts as the semantic memory layer, enabling applications such as:

Semantic Search

Document Retrieval

Recommendation Systems

Retrieval-Augmented Generation (RAG)

Agentic AI workflows

In this project, Endee is the single source of semantic truth.

📐 What is a Vector Database?

A vector database is a specialized database built to store and query vector embeddings — numerical representations of unstructured data such as:

text

documents

images

audio

code

Embedding models convert data into vectors such that:

semantically similar content → vectors close together

semantically different content → vectors far apart

Vector databases answer questions like:

“Which pieces of data are most similar in meaning to this query?”

This capability is fundamental to modern AI systems like semantic search and RAG.

🔍 How Endee Works (High-Level)

Documents are converted into vector embeddings using an embedding model

These embeddings are stored inside an Endee vector index

When a query arrives:

the query is embedded

Endee performs ANN-based similarity search

Endee returns:

top-K most relevant results

similarity scores

associated metadata (source, page number, etc.)

This enables fast, scalable, and explainable semantic retrieval, even for large document collections.

🏗 System Architecture (High Level)

The system is organized into clearly separated layers, each with a single responsibility.

┌──────────────────────────┐
│ User Interface           │
│ (Streamlit)              │
│ - Query input            │
│ - Mode selection         │
│ - Result display         │
└─────────────┬────────────┘
              ↓
┌──────────────────────────┐
│ Application Layer        │
│ (Python Backend)         │
│ - Orchestrates pipeline  │
│ - Handles modes (Search/RAG)
│ - Manages Endee client   │
└─────────────┬────────────┘
              ↓
┌──────────────────────────┐
│ Semantic Layer           │
│ (Embedding Model)        │
│ - Converts text to vectors
│ - Ensures semantic meaning
└─────────────┬────────────┘
              ↓
┌──────────────────────────┐
│ Vector Database          │
│ (Endee)                  │
│ - Stores embeddings      │
│ - Performs similarity search
│ - Returns ranked results │
└─────────────┬────────────┘
              ↓
┌──────────────────────────┐
│ Generation Layer (RAG)   │
│ (Local LLM – Ollama)     │
│ - Uses retrieved context │
│ - Generates grounded answers
└──────────────────────────┘

🔍 Semantic Search Architecture
Purpose

Retrieve relevant document passages without generation.

Pipeline
User Query
  ↓
Embedding Model
  ↓
Query Vector
  ↓
Endee Vector Database
  ↓
Top-K Similar Vectors
  ↓
Original Text + Metadata + Confidence

Characteristics

Retrieval-only (no LLM)

Fast response time

No hallucination

Fully traceable to documents

Endee is responsible for all relevance decisions.

🧠 RAG (Retrieval-Augmented Generation) Architecture
Purpose

Generate a grounded explanation using retrieved content.

Pipeline
User Question
  ↓
Embedding Model
  ↓
Query Vector
  ↓
Endee Vector Database
  ↓
Top-K Relevant Chunks
  ↓
Prompt Construction
  ↓
Local LLM (Ollama)
  ↓
Final Answer + Citations + Confidence

Key Constraint

The language model only sees content retrieved by Endee.
It never accesses raw documents directly.

This ensures:

grounded answers

reduced hallucination

explainability

📄 Document Ingestion Pipeline

Documents are processed before querying and stored semantically.

PDF / TXT Document
  ↓
Text Extraction
  ↓
Page-Aware Chunking (with overlap)
  ↓
Deduplication
  ↓
Embedding Generation
  ↓
Endee Vector Index


Each chunk is stored with metadata:

source file

page number

original text

⚙️ Project Setup & Installation
1️⃣ Start Endee (Vector Database)

Endee is run as a standalone service using Docker.

docker-compose.yml
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


Start Endee:

docker-compose up -d


Verify:

curl http://localhost:8080/api/v1/index/list


Expected output:

{"indexes":[]}

2️⃣ Install Endee Python SDK
pip install endee


The SDK provides:

index management

vector upsert & query

clean abstraction over Endee APIs

3️⃣ Configure Endee Client

The backend uses a dedicated client wrapper with safe index handling.

This ensures:

idempotent index creation

automatic recovery after restarts

no manual index management

4️⃣ Install Application Dependencies
pip install -r requirements.txt


Key dependencies:

sentence-transformers

streamlit

pypdf

requests

endee

5️⃣ Install & Run Ollama (Local LLM)

Install Ollama from:

https://ollama.com


Start the service:

ollama serve


Pull a model:

ollama pull mistral


This model is chosen for:

fast CPU inference

low memory usage

demo-friendly performance

6️⃣ Run the Application
streamlit run app.py


Access the UI at:

http://localhost:8501

▶️ Execution Order Summary

Start Endee (Docker)

Verify Endee is reachable

Install Python dependencies

Start Ollama

Run the Streamlit app

Endee must always be running before the application starts.

🔑 Key Design Choice

Endee is intentionally deployed as a separate service, mirroring real-world production systems where:

vector databases run independently

application services scale separately

retrieval remains stable across restarts
