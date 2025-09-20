from helper import load_pdf_file, text_split, download_hugging_face_embeddings
from langchain_core.vectorstores import InMemoryVectorStore

def create_in_memory_vector_store():
    extracted_data = load_pdf_file(data='data/')
    chunks = text_split(extracted_data)

    embeddings = download_hugging_face_embeddings()

    vector_store = InMemoryVectorStore.from_documents(chunks, embedding=embeddings)

    return vector_store
    