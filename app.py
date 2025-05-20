import streamlit as st
from rag_ollama import load_documents, split_documents, create_vector_store, get_context, ask_ollama, Config

st.set_page_config(page_title="Computer Security Chatbot", layout="wide")

@st.cache_resource
def init_vectorstore():
    documents = load_documents(Config.PDF_FOLDER)
    chunks = split_documents(documents)
    return create_vector_store(chunks, Config.EMBEDDING_MODEL)

st.title("🔐 Computer Security Chatbot")
st.markdown("Ask questions based on your Computer Security lecture notes.")

user_question = st.text_input("💬 Type your question:")

if user_question:
    with st.spinner("Finding the answer..."):
        vectorstore = init_vectorstore()
        context = get_context(user_question, vectorstore)

        if not context:
            st.error("Couldn't find relevant info in your lecture notes.")
        else:
            prompt = f"""
You are a helpful assistant for Computer Security students at Gazi University.
Answer the question based ONLY on the following context from lecture materials.
If the information isn't in the context, say you don't know.

Context:
{context}

Question: {user_question}

Provide a clear, concise answer with relevant details from the context:
"""
            answer = ask_ollama(prompt)
            if answer:
                st.success("🤖 Answer:")
                st.write(answer.strip())
            else:
                st.error("No response from the AI model.")
