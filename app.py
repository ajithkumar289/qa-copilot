import streamlit as st
import pandas as pd
import hashlib

from services.requirement_service import RequirementService
from services.requirement_analyzer import RequirementAnalyzerService
from services.smart_testcase_service import SmartTestCaseService
from services.document_service import DocumentService
from services.rag_service import RAGService
from utils.excel_exporter import convert_to_excel


st.set_page_config(
    page_title="QA Copilot",
    page_icon="🧪"
)

st.title("🧪 QA Copilot")


# -------------------------
# Initialize Services
# -------------------------

test_service = RequirementService()
analyzer_service = RequirementAnalyzerService()
smart_service = SmartTestCaseService()
document_service = DocumentService()
rag_service = RAGService()


# -------------------------
# Initialize Session State
# -------------------------

if "document_hash" not in st.session_state:
    st.session_state.document_hash = None

if "requirement" not in st.session_state:
    st.session_state.requirement = ""

if "chunks" not in st.session_state:
    st.session_state.chunks = []

if "embeddings" not in st.session_state:
    st.session_state.embeddings = []

if "document_stored" not in st.session_state:
    st.session_state.document_stored = False


# -------------------------
# Chat History
# -------------------------

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# -------------------------
# Upload BRD / Requirement Document
# -------------------------

uploaded_file = st.file_uploader(
    "📄 Upload BRD / Requirement Document",
    type=["pdf", "docx", "xlsx"]
)


# -------------------------
# Read Document + Chunking
# + Embeddings + ChromaDB
# -------------------------

if uploaded_file is not None:

    # Read uploaded file bytes
    file_bytes = uploaded_file.getvalue()

    # Generate hash for uploaded document
    current_document_hash = hashlib.sha256(
        file_bytes
    ).hexdigest()


    # Check if this is a new document
    if (
        st.session_state.document_hash
        != current_document_hash
    ):

        # New document detected
        st.session_state.document_hash = current_document_hash
        st.session_state.document_stored = False

        # Clear previous document data
        st.session_state.requirement = ""
        st.session_state.chunks = []
        st.session_state.embeddings = []
        # Clear previous chat
        st.session_state.chat_history = []

        with st.spinner("📖 Reading document..."):

            try:

                # Extract document text
                requirement = document_service.extract_text(
                    uploaded_file
                )


                if requirement.strip():

                    # Save requirement in session state
                    st.session_state.requirement = requirement


                    # -------------------------
                    # Phase 1: Chunking
                    # -------------------------

                    chunks = rag_service.chunk_document(
                        requirement
                    )

                    st.session_state.chunks = chunks

                    st.success(
                        f"✅ Document successfully split into "
                        f"**{len(chunks)}** chunks."
                    )


                    # -------------------------
                    # Phase 2: Embeddings
                    # -------------------------

                    with st.spinner(
                        "Generating embeddings..."
                    ):

                        embeddings = (
                            rag_service.create_embeddings(
                                chunks
                            )
                        )

                    st.session_state.embeddings = embeddings

                    st.success(
                        f"✅ Successfully generated "
                        f"**{len(embeddings)}** embeddings."
                    )


                    # -------------------------
                    # Display Embedding Dimension
                    # -------------------------

                    if len(embeddings) > 0:

                        st.info(
                            f"📐 Embedding Dimension: "
                            f"**{len(embeddings[0])}**"
                        )


                    # -------------------------
                    # Phase 3: ChromaDB Storage
                    # -------------------------

                    with st.spinner(
                        "Storing document in ChromaDB..."
                    ):

                        stored_count = (
                            rag_service.store_embeddings(
                                chunks,
                                embeddings
                            )
                        )

                    st.session_state.document_stored = True

                    st.success(
                        f"✅ Stored **{stored_count}** "
                        f"chunks in ChromaDB."
                    )


                else:

                    st.warning(
                        "The uploaded document appears "
                        "to be empty."
                    )


            except Exception as e:

                st.error(
                    f"❌ Failed to read document: {e}"
                )


    else:

        # -------------------------
        # Existing Document
        # -------------------------

        st.info(
            "📄 This document is already loaded. "
            "It will not be stored again in ChromaDB."
        )


# -------------------------
# Display Document Chunks
# -------------------------

if st.session_state.chunks:

    with st.expander(
        "📄 View Document Chunks"
    ):

        for i, chunk in enumerate(
            st.session_state.chunks,
            start=1
        ):

            st.markdown(
                f"### Chunk {i}"
            )

            st.write(chunk)

            st.divider()


# -------------------------
# BRD Semantic Search
# -------------------------

st.subheader("💬 Ask your BRD")


question = st.chat_input(
    "Enter your question"
)


if question:

    if not uploaded_file:

        st.warning(
            "Please upload a BRD before searching."
        )


    elif not question.strip():

        st.warning(
            "Please enter a question."
        )


    else:

        with st.spinner(
            "Searching relevant sections..."
        ):

            relevant_chunks = (
                rag_service.search_chunks(
                    question
                )
            )

        
        if relevant_chunks:

             context = rag_service.build_context(relevant_chunks)    

             with st.spinner("🤖 Generating AI answer..."):

                answer = test_service.answer_from_context(
                  context=context,
                  question=question
                    )

             # Save conversation
             st.session_state.chat_history.append(
                    {
                         "question": question,
                         "answer": answer
                    }     
                )
             st.subheader("💬 Conversation")

             for chat in st.session_state.chat_history:

                 with st.chat_message("user"):
                     st.write(chat["question"])

                 with st.chat_message("assistant"):
                     st.write(chat["answer"])

                 #st.divider()

                     with st.expander("📄 Retrieved Context"):

                        for i, chunk in enumerate(relevant_chunks,start=1):

                           st.markdown(f"### Chunk {i}")

                           st.write(chunk)

                           st.divider()
                 st.divider()
              

        else:

            st.warning(
                "No relevant information found."
            )
        if st.button("🗑 Clear Conversation"):

           st.session_state.chat_history = []
  
           st.rerun()


# -------------------------
# Requirement Input
# -------------------------

requirement = st.text_area(
    "Requirement / User Story",
    value=st.session_state.requirement,
    height=300,
    placeholder=(
        "Example: User should be able to "
        "login using email and password."
    )
)


# -------------------------
# Buttons
# -------------------------

col1, col2 = st.columns(2)


# -------------------------
# Analyze Requirement
# -------------------------

with col1:

    if st.button(
        "🔍 Analyze Requirement"
    ):

        if not requirement.strip():

            st.warning(
                "Please enter a requirement."
            )

        else:

            with st.spinner(
                "Analyzing requirement..."
            ):

                result = (
                    analyzer_service.analyze(
                        requirement
                    )
                )


            st.subheader(
                "📊 Requirement Analysis"
            )

            st.markdown(
                result
            )


# -------------------------
# Generate Test Cases
# -------------------------

with col2:

    if st.button(
        "🧪 Generate Test Cases"
    ):

        if not requirement.strip():

            st.warning(
                "Please enter a requirement."
            )

        else:

            with st.spinner(
                "Generating Smart Test Cases..."
            ):

                result = (
                    smart_service.generate(
                        requirement
                    )
                )


            st.subheader(
                "🧪 Test Cases"
            )


            if (
                result
                and isinstance(result, list)
            ):

                df = pd.DataFrame(
                    result
                )


                expected_columns = [

                    "test_case_id",

                    "title",

                    "category",

                    "priority",

                    "steps",

                    "expected_result"

                ]


                available_columns = [

                    col

                    for col in expected_columns

                    if col in df.columns

                ]


                df = df[
                    available_columns
                ]


                st.dataframe(
                    df,
                    use_container_width=True
                )


                # -------------------------
                # Excel Download
                # -------------------------

                excel_data = (
                    convert_to_excel(
                        result
                    )
                )


                st.download_button(

                    label=(
                        "📥 Download Test Cases "
                        "(Excel)"
                    ),

                    data=excel_data,

                    file_name=(
                        "test_cases.xlsx"
                    ),

                    mime=(
                        "application/"
                        "vnd.openxmlformats-officedocument"
                        ".spreadsheetml.sheet"
                    )

                )


            else:

                st.error(
                    "⚠️ Failed to generate "
                    "structured test cases. "
                    "Please try again."
                )