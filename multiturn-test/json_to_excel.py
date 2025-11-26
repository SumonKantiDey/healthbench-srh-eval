import pandas as pd
import json 

# Load JSON file
json_file_path = "multiturn-test/multi_turn_reponse.jsonl"
# try:
#     with open(json_file_path, "r") as f:
#         data = json.load(f)
# except Exception as e:
#     data = None
#     print(f"Failed to load JSON file: {e}")

rows = []


data = []
with open(json_file_path, 'r') as f:
    for line in f:
        data.append(json.loads(line))


srh_health_bench = pd.DataFrame(data)

# 2. Loop through each record in the list
for record_id, record in enumerate(data, start=1):
    conversation_turns = record.get("conversation_turns", [])
    prompt = record.get("prompt", [])
    prompt_id=record.get('prompt_id', None)
    response=record.get('response')

    rows.append({
        "conversation_turns": conversation_turns,
        "prompt_id": prompt_id, 
        "prompt": prompt,
        "response": response
    })

# 3. Create DataFrame
df = pd.DataFrame(rows)
df.to_excel("multiturn-test/multi_turn_reponse.xlsx", index=False)