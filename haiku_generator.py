from openai import OpenAI

client = OpenAI(
  api_key="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"
)

response = client.responses.create(
  model="gpt-5-nano",
  input="write a haiku about ai",
  store=True,
)

print(response.output_text);
