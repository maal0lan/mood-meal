import os
def fill_prompt(template_path, data):
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()
    for key, value in data.items():
        template = template.replace(f"{{{{{key}}}}}", value)
    return template
def build_prompt(ingredients, utensils, time, weather="", cuisine=""):
    data = {
        "ingredients": ingredients,
        "utensils": utensils,
        "time": time,
        "weather": weather,
        "cuisine": cuisine
    }
    template_path = os.path.join("prompts", "recipe_list_prompt.txt")
    return fill_prompt(template_path, data)