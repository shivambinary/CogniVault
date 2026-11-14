# CogniVault – AI-Powered Corporate Knowledge Assistant

## About the Project
CogniVault is an AI-powered chatbot that helps employees find information from company documents such as HR policies, leave rules, IT guidelines, and company FAQs.

It uses **Retrieval-Augmented Generation (RAG)** to retrieve relevant information from documents and generate accurate, context-based answers.

## Key Features
- Ask questions in natural language.
- Retrieve information from company documents.
- Generate answers using AI.
- Display source documents used for answers.
- Avoid unsupported answers when information is unavailable.

## Technologies Used
- Python
- Streamlit
- Sentence Transformers
- FAISS
- Large Language Model (LLM)
- RAG Architecture

## How It Works
1. Process company documents.
2. Split documents into smaller text chunks.
3. Convert chunks into embeddings.
4. Store embeddings in FAISS.
5. Retrieve relevant information based on user questions.
6. Generate answers using an LLM.

## Dataset
The project uses a synthetic corporate knowledge base created for demonstration and academic purposes.

## Goal
To build a simple AI assistant that makes company information easier to access, understand, and search.

