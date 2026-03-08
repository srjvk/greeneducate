from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
import os, hashlib

VECTORSTORE_PATH = os.getenv("VECTORSTORE_PATH","./vectorstore")
EMBED_MODEL = os.getenv("EMBED_MODEL","nomic-embed-text")

def get_embeddings():
    return OllamaEmbeddings(model=EMBED_MODEL)

def ingest_pdf(pdf_path: str) -> dict:
    loader = PyPDFLoader(pdf_path)
    pages = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800, chunk_overlap = 100
    )

    chunks = splitter.split_documents(pages)

    doc_id = hashlib.md5(open(pdf_path,"rb").read()).hexdigest()[:12]
    collection_name = f"currciculum_{doc_id}"

    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=get_embeddings(),
        persist_directory=VECTORSTORE_PATH,
        collection_name=collection_name,
    )
    vectordb.persist()

    return {
        "doc_id": doc_id,
        "collection": collection_name,
        "pages": len(pages),
        "chunks": len(chunks),
    }

def retrieve(query: str, collection_name: str, k: int = 5) -> list[str]:
    vectordb = Chroma(
        persist_directory = VECTORSTORE_PATH,
        embedding_function = get_embeddings(),
        collection_name = collection_name,
    )
    docs = vectordb.similarity_search(query, k = k)
    return [d.page_content for d in docs]

