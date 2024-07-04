# PDF-Reader-Answer-Assistant

This FastAPI application allows users to upload PDF files and ask questions about the content within them. 
The application processes the PDF files, extracts text, and uses Google Generative AI to answer user questions based on the content of the uploaded PDFs.

## Features

- Upload PDF files and extract text content.
- Use Google Generative AI to answer questions based on the content of uploaded PDFs.
- CORS support for communication with a front-end application.

## Setup Instructions

### Prerequisites

Back-End,

- Python 3.11
- Pip (Python package installer)
- FastAPI
- Uvicorn (ASGI server)

Front-End,

- React.js
- Node 
- Npm
- Axios


LLM.

- google_generativeai
- python-dotenv
- langchain
- PyPDF2
- faiss-cpu
- langchain_google_genai

Environment Variables
GOOGLE_API_KEY: Your Google API key for accessing Google Generative AI services.

GOOGLE_API_KEY=your_actual_api_key_here


## API Documentation

Endpoints

Root
URL: /
Method: GET
Description: Returns a welcome message.
Response:
200 OK: {"message": "Welcome to the PDF Q&A API"}

Upload PDF
URL: /upload/
Method: POST
Description: Uploads a PDF file and processes its text content.
Request:
file: PDF file to upload.
Response:
200 OK: {"filename": "uploaded_file.pdf", "message": "PDF processed successfully"}
500 Internal Server Error: {"detail": "Failed to process PDF: <error_message>"}

Ask Question
URL: /question/
Method: POST
Description: Ask a question based on the content of the uploaded PDFs.
Request:
question: The question to ask.
Response:
200 OK: {"question": "<question>", "answer": "<answer>"}
500 Internal Server Error: {"detail": "Failed to process question: <error_message>"}

##  Application Architecture
- FastAPI: The web framework used to build the API.
- Uvicorn: ASGI server to run the FastAPI application.
- Google Generative AI: Used to generate answers based on the content of the PDFs.
- PyPDF2: Library to read and extract text from PDF files.
- LangChain: Framework for building applications with language models.
- FAISS: Library for efficient similarity search and clustering of dense vectors.
