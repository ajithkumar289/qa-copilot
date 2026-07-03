import streamlit as st

from services.requirement_service import RequirementService
from services.requirement_analyzer import RequirementAnalyzerService

st.set_page_config(page_title="QA Copilot", page_icon="🧪")

st.title("🧪 QA Copilot")

requirement = st.text_area(
    "Enter Requirement / User Story",
    height=200,
    placeholder="Example: User should be able to login using email and password."
)

col1, col2 = st.columns(2)

test_service = RequirementService()
analyzer_service = RequirementAnalyzerService()

# -------------------------
# BUTTON 1: ANALYZE
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
# BUTTON 2: GENERATE TEST CASES
# -------------------------
with col2:
    if st.button("🧪 Generate Test Cases"):

        if not requirement.strip():
            st.warning("Please enter a requirement.")
        else:
            with st.spinner("Generating test cases..."):
                result = test_service.generate_test_cases(requirement)
                st.subheader("🧪 Test Cases")
                st.markdown(result)