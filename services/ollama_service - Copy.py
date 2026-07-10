from langchain_text_splitters import RecursiveCharacterTextSplitter


class RAGService:
    """
    Handles document chunking for Retrieval-Augmented Generation (RAG).
    """

    @staticmethod
    def chunk_document(text):
        """
        Splits a document into overlapping chunks.

        Args:
            text (str): Extracted document text.

        Returns:
            list[str]: List of text chunks.
        """

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=150,
            length_function=len
        )

        chunks = splitter.split_text(text)

        return chunks