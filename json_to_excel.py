import pandas as pd
import json 

# Load JSON file
# json_file_path = "./data/gpt4_grader.json"  # Change this to your actual path
json_file_path = "./data/gpt4_grader_gpt4o_nano_response.json"
try:
    with open(json_file_path, "r") as f:
        data = json.load(f)
except Exception as e:
    data = None
    print(f"Failed to load JSON file: {e}")

rows = []

# 2. Loop through each record in the list
for record_id, record in enumerate(data, start=1):
    conversations = record.get("conversations", [])
    rubrics = record.get("rubrics", [])
    prompt_id=record.get('prompt_id', None)
    total=record.get('total')

    # Extract the first user and assistant messages
    user_text = None
    assistant_text = None
    for msg in conversations:
        if msg.get("role") == "user" and user_text is None:
            user_text = msg.get("content")
        elif msg.get("role") == "assistant" and assistant_text is None:
            assistant_text = msg.get("content")

    # Loop through rubrics and make rows
    for rubric in rubrics:
        rows.append({
            "Record ID": record_id,
            "prompt_id": prompt_id, 
            "User Message": user_text,
            "Assistant Message": assistant_text,
            "Criteria": rubric.get("criteria"),
            "Points Possible": rubric.get("points"),
            "Criteria Met": rubric.get("criteria_met"),
            "Score": rubric.get("score"),
            "Explanation": rubric.get("explanation"),
            "total": total
        })

# 3. Create DataFrame
df = pd.DataFrame(rows)
# 4. Save to Excel
# df.to_excel("./data/gpt4_grader.xlsx", index=False)
df.to_excel("./data/gpt4_grader_gpt4o_nano_response.xlsx", index=False)
