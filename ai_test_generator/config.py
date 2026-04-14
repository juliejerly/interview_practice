from groq import Groq
import os
# -----------------------------
# AI CONFIGURATION
# -----------------------------
client = Groq(
    api_key=os.getenv("OPENAI_API_KEY")
)
AI_MODEL = "llama-3.3-70b-versatile"

# -----------------------------
# JIRA CONFIGURATION
# -----------------------------
JIRA_URL = os.getenv("JIRA_URL")
#ISSUE_KEY = "IQPS-69"

EMAIL = os.getenv("EMAIL_ID")
API_TOKEN = os.getenv("JIRA_API_TOKEN")