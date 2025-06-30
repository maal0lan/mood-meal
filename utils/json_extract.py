import re
import json

def extract_json_block(text):
    """
    Extracts the last valid JSON object from a Falcon-style model output.
    """
    try:
        matches = re.findall(r'{[\s\S]+}', text)
        for match in reversed(matches):
            try:
                return json.loads(match)
            except json.JSONDecodeError:
                continue
    except Exception as e:
        raise ValueError(f"Failed to extract JSON: {e}")
    
    raise ValueError("No valid JSON found in the response.")
