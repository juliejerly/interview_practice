import streamlit as st
import config
from jira_client import get_jira_story
from ai_generate_tests import generate_test_cases
from utils.excel_helper import export_test_cases_to_excel
from PyPDF2 import PdfReader
from docx import Document

st.title("AI Test Case Generator")

st.write("Generate test cases from Jira OR upload a requirements document")

# -------------------------
# INPUT OPTIONS
# -------------------------

jira_id = st.text_input("Enter JIRA Issue Key (Example: QA-101)")

uploaded_file = st.file_uploader(
    "OR Upload Requirement Document",
    type=["txt", "pdf", "docx"]
)

# -------------------------
# GENERATE BUTTON
# -------------------------

if st.button("Generate Test Cases"):

    summary = ""
    description = ""

    # OPTION 1 — JIRA
    if jira_id:

        st.write("Fetching user story from Jira...")

        summary, description = get_jira_story(
            config.JIRA_URL,
            jira_id,
            config.EMAIL,
            config.API_TOKEN
        )

    # OPTION 2 — DOCUMENT
    elif uploaded_file:

        file_type = uploaded_file.name.split(".")[-1]
        # TEXT FILE
        if file_type == "txt":
            description = uploaded_file.read().decode("utf-8")

        # PDF FILE
        elif file_type == "pdf":
            pdf = PdfReader(uploaded_file)
            for page in pdf.pages:
                description += page.extract_text()

        # WORD FILE
        elif file_type == "docx":
            doc = Document(uploaded_file)
            for para in doc.paragraphs:
                description += para.text + "\n"


        summary = uploaded_file.name
        #description = file_content

    else:
        st.warning("Please enter a JIRA ID or upload a file")
        st.stop()

    # -------------------------
    # SHOW INPUT
    # -------------------------

    st.subheader("Summary")
    st.write(summary)

    st.subheader("Description")
    st.write(description)

    # -------------------------
    # AI GENERATION
    # -------------------------

    st.write("Generating AI Test Cases...")

    test_cases = generate_test_cases(summary, description)

    file_id = jira_id if jira_id else "Uploaded_Doc"

    export_test_cases_to_excel(test_cases, file_id)

    st.success("✅ Test cases generated and Excel file created!")