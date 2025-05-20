import os
import logging
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import requests
from typing import List, Optional

# =================== SETUP LOGGING ===================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("rag_log.txt"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


# =================== CONFIG ===================
class Config:
    PDF_FOLDER = "C:/Users/brakc/Burak/Computer Science/GaziU/3.2/ceng374_int_to_computer_security/project-1/RAG-Computer_Security_Chatbot/pdfs"
    EMBEDDING_MODEL = "BAAI/bge-base-en-v1.5"
    OLLAMA_URL = "http://localhost:11434/api/generate"
    OLLAMA_MODEL = "deepseek-r1:1.5b"
    CHUNK_SIZE = 500
    CHUNK_OVERLAP = 100
    TOP_K_CONTEXT = 5  # Increased from 3 to get more relevant context


# =================== DOCUMENT PROCESSING ===================
def load_documents(pdf_folder: str) -> List:
    """Load all PDF documents from the specified folder."""
    logger.info("Loading PDF documents...")
    documents = []

    if not os.path.exists(pdf_folder):
        logger.error(f"PDF folder not found: {pdf_folder}")
        raise FileNotFoundError(f"PDF folder not found: {pdf_folder}")

    for filename in os.listdir(pdf_folder):
        if filename.endswith(".pdf"):
            full_path = os.path.join(pdf_folder, filename)
            logger.info(f"Loading: {filename}")
            try:
                loader = PyPDFLoader(full_path)
                documents.extend(loader.load())
            except Exception as e:
                logger.error(f"Failed to load {filename}: {e}")
                continue

    logger.info(f"Total documents loaded: {len(documents)}")
    return documents


def split_documents(documents: List) -> List:
    """Split documents into chunks for processing."""
    logger.info("Splitting documents into chunks...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=Config.CHUNK_SIZE,
        chunk_overlap=Config.CHUNK_OVERLAP
    )
    chunks = splitter.split_documents(documents)
    logger.info(f"Total chunks created: {len(chunks)}")
    return chunks


# =================== VECTOR STORE ===================
def create_vector_store(chunks: List, embedding_model: str):
    """Create and return a FAISS vector store."""
    logger.info(f"Loading embedding model: {embedding_model}")
    embedding = HuggingFaceEmbeddings(model_name=embedding_model)

    logger.info("Creating FAISS vector store...")
    try:
        vectorstore = FAISS.from_documents(chunks, embedding)
        logger.info("Vector store created successfully.")
        return vectorstore
    except Exception as e:
        logger.error(f"Failed to create vector store: {e}")
        raise


# =================== QUERY PROCESSING ===================
def get_context(query: str, vectorstore, top_k: int = Config.TOP_K_CONTEXT) -> str:
    """Retrieve relevant context for a query."""
    logger.info(f"Searching context for query: {query}")
    try:
        results = vectorstore.similarity_search(query, k=top_k)
        return "\n\n".join([doc.page_content for doc in results])
    except Exception as e:
        logger.error(f"Context search failed: {e}")
        return ""


def ask_ollama(prompt: str) -> Optional[str]:
    """Send prompt to Ollama and return the response."""
    logger.info("Sending request to Ollama model...")
    try:
        response = requests.post(
            Config.OLLAMA_URL,
            json={
                "model": Config.OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False
            },
            timeout=90  # Added timeout
        )
        response.raise_for_status()
        logger.info("Response received from Ollama.")
        return response.json().get("response")
    except requests.exceptions.RequestException as e:
        logger.error(f"Ollama request failed: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return None


# =================== MAIN ===================
def main():
    try:
        # Load and process documents
        documents = load_documents(Config.PDF_FOLDER)
        if not documents:
            logger.error("No documents loaded. Exiting.")
            return

        chunks = split_documents(documents)
        vectorstore = create_vector_store(chunks, Config.EMBEDDING_MODEL)

        # Main interaction loop
        while True:
            user_question = input(
                "\n🔎 Ask a question about your Computer Security lectures (or type 'exit' to quit):\n> ")

            if user_question.lower() in ['exit', 'quit']:
                break

            logger.info(f"User question: {user_question}")

            # Get context and generate answer
            context = get_context(user_question, vectorstore)

            if not context:
                print("\n🤖 I couldn't find relevant information in the lecture materials.")
                continue

            final_prompt = f"""
You are a helpful assistant for Computer Security students at Gazi University.
Answer the question based ONLY on the following context from lecture materials.
If the information isn't in the context, say you don't know.

Context:
{context}

Question: {user_question}

Provide a clear, concise answer with relevant details from the context:
"""

            answer = ask_ollama(final_prompt)

            if answer:
                print("\n🤖 Ollama says:\n")
                print(answer.strip())
                logger.info("Answer delivered to user.")
            else:
                print("\n⚠️ Sorry, I couldn't get a response from the AI model.")

    except Exception as e:
        logger.error(f"Fatal error: {e}")
        print("\n⚠️ An error occurred. Please check the logs for details.")


if __name__ == "__main__":
    main()