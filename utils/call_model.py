import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()

client = InferenceClient(
    provider="novita",
    api_key=os.getenv("HG_TOKEN")
)

def call_model(user_prompt):
    system_prompt = (
        "You are an AI chef. Based on the user's input, return ONLY valid JSON. "
        "No explanation. No markdown. No input echoing. No preamble.\n\n"
        "Format:\n"
        '{\n  "recipes": [...],\n  "suggestions": [...]\n}'
    )

    completion = client.chat.completions.create(
        model="mistralai/Mistral-7B-Instruct-v0.3",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7
    )

    return completion.choices[0].message.content.strip()
