import streamlit as st

from config import APP_TITLE
from services.requirement_service import RequirementService

st.set_page_config(page_title="QA Copilot", page_icon="🧪")

st.title(APP_TITLE)

st.write("Generate QA Test Cases using Ollama + Qwen")

requirement = st.text_area(
    "Enter Requirement / User Story",
    height=200,
    placeholder="Example: User should be able to login using email and password."
)

service = RequirementService()

if st.button("Generate Test Cases"):

    if not requirement.strip():

        st.warning("Please enter a requirement.")

    else:

        try:

            with st.spinner("Generating test cases..."):

                result = service.generate_test_cases(requirement)

                st.markdown(result)

        except Exception as e:

            st.error(e)