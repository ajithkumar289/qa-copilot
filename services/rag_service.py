import streamlit as st
import chromadb

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
    Handles Retrieval-Augmented Generation (RAG).

    Features:
    - Document Chunking
    - Embedding Generation
    - Document-aware ChromaDB Storage
    - Duplicate Document Protection
    - Document-specific Semantic Search
    - Retrieval Relevance Filtering
    - Context Construction
    """

    def __init__(self):

        self.embedding_model = load_embedding_model()

        self.collection = load_chroma_collection()

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=150,
            length_function=len
        )

    # --------------------------------------------------
    # Chunking
    # --------------------------------------------------

    def chunk_document(self, text):
        """
        Split document into overlapping chunks.
        """

        if not text or not text.strip():
            return []

        return self.text_splitter.split_text(text)

    # --------------------------------------------------
    # Embeddings
    # --------------------------------------------------

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

    # --------------------------------------------------
    # Check Existing Document
    # --------------------------------------------------

    def document_exists(self, document_hash):
        """
        Check whether a document already exists in ChromaDB.
        """

        if not document_hash:
            return False

        results = self.collection.get(
            where={
                "document_hash": document_hash
            },
            limit=1
        )

        return bool(results.get("ids"))

    # --------------------------------------------------
    # Store Embeddings
    # --------------------------------------------------

    def store_embeddings(
        self,
        chunks,
        embeddings,
        document_hash,
        document_name=None
    ):
        """
        Store document chunks and embeddings in ChromaDB.

        Uses document hash to prevent duplicate storage.
        """

        if not chunks or len(embeddings) == 0:
            return 0

        if not document_hash:
            raise ValueError(
                "Document hash is required for storing embeddings."
            )

        # Prevent duplicate document storage
        if self.document_exists(document_hash):
            return 0

        document_id = document_hash[:16]

        ids = [
            f"{document_id}_chunk_{i}"
            for i in range(len(chunks))
        ]

        metadatas = [
            {
                "document_id": document_id,
                "document_hash": document_hash,
                "document_name": document_name or "Uploaded BRD",
                "chunk_number": i
            }
            for i in range(len(chunks))
        ]

        self.collection.add(
            ids=ids,
            documents=chunks,
            embeddings=embeddings.tolist(),
            metadatas=metadatas
        )

        return len(chunks)

    # --------------------------------------------------
    # Semantic Search + Relevance Filtering
    # --------------------------------------------------

    def search_chunks(
        self,
        question,
        document_hash,
        top_k=5,
        min_similarity=0.35
    ):
        """
        Retrieve relevant chunks only from the
        currently uploaded document.

        Chunks below the minimum cosine similarity
        threshold are ignored.
        """

        if not question or not question.strip():
            return []

        if not document_hash:
            return []

        # Convert question into embedding
        question_embedding = self.embedding_model.encode(
            question,
            convert_to_numpy=True
        )

        # Search only inside current BRD
        results = self.collection.query(
            query_embeddings=[
                question_embedding.tolist()
            ],
            n_results=top_k,
            where={
                "document_hash": document_hash
            },
            include=[
                "documents",
                "embeddings"
            ]
        )

        documents = results.get("documents", [])
        embeddings = results.get("embeddings", [])

        if not documents or not embeddings:
            return []

        retrieved_documents = documents[0]
        retrieved_embeddings = embeddings[0]

        relevant_chunks = []

        # Calculate cosine similarity
        for document, embedding in zip(
            retrieved_documents,
            retrieved_embeddings
        ):

            similarity = (
                question_embedding @ embedding
            ) / (
                (
                    question_embedding @ question_embedding
                ) ** 0.5
                *
                (
                    embedding @ embedding
                ) ** 0.5
            )

            if similarity >= min_similarity:
                relevant_chunks.append(document)

        return relevant_chunks

    # --------------------------------------------------
    # Build Context
    # --------------------------------------------------

    def build_context(self, chunks):
        """
        Combine retrieved chunks into a single context.
        """

        if not chunks:
            return ""

        return "\n\n".join(chunks)