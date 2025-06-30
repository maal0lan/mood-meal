from utils.format_input import build_prompt
from utils.call_model import call_model
from utils.generate_instructions import generate_detailed_steps
from utils.json_extract import extract_json_block
import json
import argparse
import re
def extract_json(text):
    match = re.search(r'\{(?:.|\n)*?\}', text)
    if match:
        return match.group()
    else:
        raise ValueError("No JSON found in model response.")
parser = argparse.ArgumentParser(description="MoodMeal CLI")
parser.add_argument("--ingredients", type=str, required=True, help="Comma-separated ingredients")
parser.add_argument("--utensils", type=str, default="", help="Comma-separated utensils")
parser.add_argument("--time", type=str, required=True, help="Time available to cook")
parser.add_argument("--weather", type=str, default="", help="Weather condition")
parser.add_argument("--cuisine", type=str, default="", help="Optional cuisine type")
args = parser.parse_args()
prompt = build_prompt(
    ingredients=args.ingredients,
    utensils=args.utensils,
    time=args.time,
    weather=args.weather,
    cuisine=args.cuisine
)
response = call_model(prompt)
print("\n RAW RESPONSE:\n", response)
try:
    json_string = extract_json(response)
    json_data = extract_json_block(response)

    print("\n Available Recipes:")
    for i, r in enumerate(json_data["recipes"], 1):
        print(f"{i}. {r['name']} ({r['cook_time']})")

    choice = input("\n Type the name of the recipe you want to cook: ").strip()
    selected = next((r for r in json_data["recipes"] if r["name"].lower() == choice.lower()), None)

    if selected:
        print(f"\n Generating steps for {selected['name']}...")
        steps_response = generate_detailed_steps(
            recipe_name=selected["name"],
            ingredients=", ".join(selected["ingredients_used"]),
            cook_time=selected["cook_time"]
        )


        try:
            steps_json_string = extract_json(steps_response)
            steps_json = json.loads(steps_json_string)
            print(json.dumps(steps_json, indent=2))
        except Exception as e:
            print(" Failed to parse steps JSON:", e)
            print(steps_response)
    else:
        print(" Recipe not found. Please type exactly as shown.")

except Exception as e:
    print(" JSON Parsing Error:", e)
    print(response)
