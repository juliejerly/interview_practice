#===============================================================
#Holds configuration & runs workflow
#================================================================

from jira_client import get_jira_story
from ai_generate_tests import generate_test_cases
from utils.excel_helper import export_test_cases_to_excel
import config


jira_id=config.ISSUE_KEY
summary, description = get_jira_story(
    config.JIRA_URL,
    jira_id,
    config.EMAIL,
    config.API_TOKEN
)


# -----------------------------
# GENERATE TEST CASES
# -----------------------------
test_cases = generate_test_cases(summary, description)
  
print("\n===== USER STORY =====\n")
print("Summary:", summary)
print("\nDescription:", description)

# -----------------------------
# EXPORT TO EXCEL
# -----------------------------
export_test_cases_to_excel(test_cases, jira_id)