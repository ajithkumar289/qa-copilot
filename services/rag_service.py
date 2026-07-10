from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter


class RAGService:
    """
    Handles all Retrieval-Augmented Generation (RAG) operations.

    Current Phase:
    - Document Chunking
    - Embedding Generation

    Upcoming Phases:
    - ChromaDB Storage
    - Semantic Search
    - Question Answering
    """

    def __init__(self):
        """
        Load embedding model only once.
        """
        self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

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