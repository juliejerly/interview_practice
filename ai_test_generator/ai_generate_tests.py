from groq import Groq
import config
import json
import re

# -----------------------------
# GENERATE TEST CASES USING AI
# -----------------------------

def generate_test_cases(story_summary, description_text):
    prompt = f"""
    You are a QA engineer.
    Generate detailed manual test cases for the following user story.

    Summary:
    {story_summary}

    Description:
    {description_text}

    Instructions:
    1. Identify functional scenarios
    2. Include positive cases
    3. Include negative cases
    4. Include edge cases
    5. Include validation scenarios

    Include:
    Test Case ID
    Test Scenario
    Preconditions
    Test Steps
    Expected Result
    Test Type

    Return the output strictly in JSON format like this:

    [
      {{
        "test_case_id": "TC_01",
        "test_scenario": "",
        "preconditions": "",
        "test_steps": ["", "", ""],
        "expected_result": "",
        "test_type": "Positive/Negative/Edge"
      }}
    ]

    """

    response = config.client.chat.completions.create(
        model=config.AI_MODEL,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    ai_output = response.choices[0].message.content
    # Remove markdown formatting if present
    ai_output = ai_output.replace("```json", "").replace("```", "").strip()
    # Remove trailing commas before ] or }
    ai_output = re.sub(r",\s*([\]}])", r"\1", ai_output)
    print("AI OUTPUT:", ai_output)
    test_cases = json.loads(ai_output)
    return test_cases
