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


