import logging
from fastapi import FastAPI, HTTPException, UploadFile, File
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os
import google.generativeai as genai
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Add this before defining your FastAPI app
origins = [
    "http://localhost",
    "http://localhost:3000",  # Update with your frontend URL
    # Add more origins as needed, e.g., for different environments
]

app = FastAPI()

# Add CORS middleware with specific origins and other settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],  # Adjust based on your API's requirements
    allow_headers=["*"],  # Adjust based on your API's headers
)

load_dotenv()
GOOGLE_API_KEY = os.getenv('google_api_key')
if not GOOGLE_API_KEY:
    logging.error("Google API Key is not set. Please check your .env file.")
else:
    genai.configure(api_key=GOOGLE_API_KEY)


def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks

def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")
    return vector_store

def get_conversational_chain():
    prompt_template = """
    Answer the question as detailed as possible from the provided context. If the answer is not in
    the provided context, say "answer is not available in the context" and don't provide a wrong answer.

    Context:
    {context}

    Question:
    {question}

    Answer:
    """
    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    return chain

class QuestionRequest(BaseModel):
    question: str

@app.get("/")
async def root():
    return {"message": "Welcome to the PDF Q&A API"}

@app.post("/upload/")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        content = await file.read()
        text = get_pdf_text([file.file])
        text_chunks = get_text_chunks(text)
        get_vector_store(text_chunks)
        return {"filename": file.filename, "message": "PDF processed successfully"}
    except Exception as e:
        logging.error(f"Error processing PDF: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to process PDF: {str(e)}")
    


@app.post("/question/")
async def ask_question(request: QuestionRequest):
    try:
        question = request.question
        logging.info(f"Received question: {question}")

        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        vector_store = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
        context = vector_store.similarity_search(question, k=5)

        logging.info(f"Context found: {context}")

        chain = get_conversational_chain()
        response = chain({"input_documents": context, "question": question}, return_only_outputs=True)

        if response:
            return {"question": question, "answer": response["output_text"]}
        else:
            return {"question": question, "answer": "No answer found."}

    except Exception as e:
        logging.error(f"Error processing question: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to process question: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
