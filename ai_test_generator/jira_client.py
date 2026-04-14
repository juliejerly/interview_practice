#===============================================
#Fetches story from JIRA
#================================================
import requests
from requests.auth import HTTPBasicAuth
import os

# -----------------------------
# FUNCTION TO CONVERT JIRA ADF
# -----------------------------
def extract_text_from_adf(adf):

    text = ""

    if not adf:
        return text

    def parse_content(content):

        result = ""

        for item in content:

            if item["type"] == "paragraph":
                if "content" in item:
                    for sub in item["content"]:
                        if sub["type"] == "text":
                            result += sub["text"]
                        elif sub["type"] == "inlineCard":
                            result += sub["attrs"]["url"]

                result += "\n"

            elif item["type"] == "orderedList":

                counter = 1

                for li in item["content"]:
                    result += f"{counter}. "

                    if "content" in li:
                        result += parse_content(li["content"])

                    counter += 1

            elif item["type"] == "bulletList":

                for li in item["content"]:
                    result += "- "

                    if "content" in li:
                        result += parse_content(li["content"])

        return result

    text = parse_content(adf["content"])

    return text
# -----------------------------
# API CALL
# -----------------------------
def get_jira_story(jira_url, issue_key, email, api_token):
    auth = HTTPBasicAuth(email, api_token)
    url = f"{jira_url}/rest/api/3/issue/{issue_key}"
    print(f" Auth details: {auth.username} {auth.password}")
    print("URL :" , url)

    headers = {
        "Accept": "application/json"
    }

    response = requests.get(url, headers=headers, auth=auth)
    print(response)
    if response.status_code != 200:
        raise Exception(f"Error fetching issue: {response.text}")
    
    data = response.json()
    story_summary = data["fields"]["summary"]
    story_description = data["fields"]["description"]

    description_text = extract_text_from_adf(story_description)

    return story_summary, description_text