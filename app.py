import streamlit as st
import pandas as pd

from services.requirement_service import RequirementService
from services.requirement_analyzer import RequirementAnalyzerService
from services.smart_testcase_service import SmartTestCaseService
from utils.excel_exporter import convert_to_excel

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
smart_service = SmartTestCaseService()

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
            with st.spinner("Generating smart test cases..."):
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

                df = df[[col for col in expected_columns if col in df.columns]]

                st.dataframe(df, use_container_width=True)

                # Download Excel
                excel_data = convert_to_excel(result)

                st.download_button(
                    label="📥 Download Test Cases (Excel)",
                    data=excel_data,
                    file_name="test_cases.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

            else:
                st.error("⚠️ Failed to generate structured test cases. Please try again.")