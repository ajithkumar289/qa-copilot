import streamlit as st
import pandas as pd

from services.requirement_service import RequirementService
from services.requirement_analyzer import RequirementAnalyzerService
from services.smart_testcase_service import SmartTestCaseService
from services.document_service import DocumentService
from services.rag_service import RAGService
from utils.excel_exporter import convert_to_excel

st.set_page_config(page_title="QA Copilot", page_icon="🧪")

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
# Upload BRD / Requirement Document
# -------------------------
uploaded_file = st.file_uploader(
    "📄 Upload BRD / Requirement Document",
    type=["pdf", "docx", "xlsx"]
)

# -------------------------
# Read Document + Chunking + Embeddings
# -------------------------
requirement = ""
chunks = []
embeddings = []

if uploaded_file is not None:
    with st.spinner("📖 Reading document..."):
        try:
            requirement = document_service.extract_text(uploaded_file)

            if requirement.strip():

                # Chunk the document
                chunks = rag_service.chunk_document(requirement)

                st.success(
                    f"✅ Document successfully split into **{len(chunks)}** chunks."
                )

                # Generate embeddings
                with st.spinner("Generating embeddings..."):
                    embeddings = rag_service.create_embeddings(chunks)
                    stored_count = rag_service.store_embeddings(chunks,embeddings)
                st.success( f"✅ Stored {stored_count} chunks in ChromaDB.")	  

                st.success(
                    f"✅ Successfully generated **{len(embeddings)}** embeddings."
                )

                # Display embedding dimension
                if len(embeddings) > 0:
                    st.info(
                        f"📐 Embedding Dimension: **{len(embeddings[0])}**"
                    )

                # Display chunks
                with st.expander("📄 View Document Chunks"):

                    for i, chunk in enumerate(chunks, start=1):
                        st.markdown(f"### Chunk {i}")
                        st.write(chunk)
                        st.divider()

            else:
                st.warning("The uploaded document appears to be empty.")

        except Exception as e:
            st.error(f"❌ Failed to read document: {e}")

# -------------------------
# Requirement Input
# -------------------------
requirement = st.text_area(
    "Requirement / User Story",
    value=requirement,
    height=300,
    placeholder="Example: User should be able to login using email and password."
)

# -------------------------
# Buttons
# -------------------------
col1, col2 = st.columns(2)

# -------------------------
# Analyze Requirement
# -------------------------
with col1:

    if st.button("🔍 Analyze Requirement"):

        if not requirement.strip():
            st.warning("Please enter a requirement.")

        else:
            with st.spinner("Analyzing requirement..."):
                result = analyzer_service.analyze(requirement)

            st.subheader("📊 Requirement Analysis")
            st.markdown(result)

# -------------------------
# Generate Test Cases
# -------------------------
with col2:

    if st.button("🧪 Generate Test Cases"):

        if not requirement.strip():
            st.warning("Please enter a requirement.")

        else:
            with st.spinner("Generating Smart Test Cases..."):
                result = smart_service.generate(requirement)

            st.subheader("🧪 Test Cases")

            if result and isinstance(result, list):

                df = pd.DataFrame(result)

                expected_columns = [
                    "test_case_id",
                    "title",
                    "category",
                    "priority",
                    "steps",
                    "expected_result"
                ]

                available_columns = [
                    col for col in expected_columns if col in df.columns
                ]

                df = df[available_columns]

                st.dataframe(
                    df,
                    use_container_width=True
                )

                # -------------------------
                # Excel Download
                # -------------------------
                excel_data = convert_to_excel(result)

                st.download_button(
                    label="📥 Download Test Cases (Excel)",
                    data=excel_data,
                    file_name="test_cases.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

            else:
                st.error(
                    "⚠️ Failed to generate structured test cases. Please try again."
                )