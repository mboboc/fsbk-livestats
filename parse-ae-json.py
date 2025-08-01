# %%

import json


def replace_lottie_text(input_path, output_path, old_text, new_text):
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Traverse layers and replace text
    for layer in data.get("layers", []):
        if layer.get("ty") == 5:  # 'ty' == 5 indicates a text layer
            try:
                text_data = layer["t"]["d"]["k"][0]["s"]
                if text_data.get("t") == old_text:
                    text_data["t"] = new_text
            except (KeyError, IndexError):
                continue

    # Save the modified JSON
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# Example usage
replace_lottie_text("data-original.json", "data.json", "TEXT1", "1:60;34")