import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from utils.format_input import fill_prompt

load_dotenv()

client = InferenceClient(
    provider="novita",
    api_key=os.getenv("HG_TOKEN")
)

def generate_detailed_steps(recipe_name, ingredients, cook_time):
    system_prompt = (
        "You are a cooking assistant. Only return valid JSON with step-by-step instructions. "
        "No intro, no markdown. Assume salt, oil, and sugar are always available.\n\n"
        'Format:\n{ "name": "", "steps": ["", "", ...] }'
    )

    user_prompt = fill_prompt(
        os.path.join("prompts", "recipe_detial_prompt.txt"),
        {
            "recipe_name": recipe_name,
            "ingredients": ingredients,
            "cook_time": cook_time
        }
    )

    completion = client.chat.completions.create(
        model="mistralai/Mistral-7B-Instruct-v0.3",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.6
    )

    return completion.choices[0].message.content.strip()
