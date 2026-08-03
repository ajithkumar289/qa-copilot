import streamlit as st
import chromadb
import uuid

from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter


@st.cache_resource
def load_embedding_model():
    """
    Load embedding model only once.
    """
    return SentenceTransformer("all-MiniLM-L6-v2")


@st.cache_resource
def load_chroma_collection():
    """
    Initialize persistent ChromaDB collection.
    """

    client = chromadb.PersistentClient(
        path="data/chroma_db"
    )

    collection = client.get_or_create_collection(
        name="qa_copilot_brd"
    )

    return collection


class RAGService:
    """
    Handles all Retrieval-Augmented Generation (RAG) operations.

    Completed:
    - Document Chunking
    - Embedding Generation
    - ChromaDB Storage

    Current Phase:
    - Unique Document Storage

    Upcoming:
    - Semantic Search
    - Question Answering
    """

    def __init__(self):

        self.embedding_model = load_embedding_model()

        self.collection = load_chroma_collection()

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=150,
            length_function=len
        )


    def chunk_document(self, text):
        """
        Split document into overlapping chunks.
        """

        if not text or not text.strip():
            return []

        return self.text_splitter.split_text(text)


    def create_embeddings(self, chunks):
        """
        Generate embeddings for document chunks.
        """

        if not chunks:
            return []

        embeddings = self.embedding_model.encode(
            chunks,
            convert_to_numpy=True
        )

        return embeddings


    def generate_document_id(self):
        """
        Generate unique ID for every uploaded document.
        """

        return str(uuid.uuid4())[:8]


    def store_embeddings(self, chunks, embeddings):
        """
        Store document chunks and embeddings into ChromaDB.
        """

        if not chunks or len(embeddings) == 0:
            return 0

        document_id = self.generate_document_id()

        ids = [
            f"{document_id}_chunk_{i}"
            for i in range(len(chunks))
        ]

        self.collection.add(
            ids=ids,
            documents=chunks,
            embeddings=embeddings.tolist(),
            metadatas=[
                {
                    "document_id": document_id,
                    "chunk_number": i
                }
                for i in range(len(chunks))
            ]
        )

        return len(chunks)
    def search_chunks(self, question, top_k=5):
        """
        Retrieve most relevant chunks from ChromaDB.
        """

        if not question or not question.strip():
            return []

        # Convert question into embedding
        question_embedding = self.embedding_model.encode(
            question,
            convert_to_numpy=True
        )

        # Search ChromaDB
        results = self.collection.query(
            query_embeddings=[
                question_embedding.tolist()
            ],
            n_results=top_k
        )

        documents = results.get("documents", [])

        if documents:
            return documents[0]

        return []
    def build_context(self, chunks):
        """
        Combine retrieved chunks into a single context.
        """

        if not chunks:
           return ""

        return "\n\n".join(chunks)