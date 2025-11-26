import pandas as pd 
import openai, ast
import json
import os 
from tqdm import tqdm
import time 

from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("myna_openai")

openai.api_key = API_KEY

# === Input and Output Settings ===
input_csv = "data/health_bench_for_srh.csv"
text_column = "prompt"     
output_json = "multiturn-test/multi_turn_reponse.jsonl"

# === Auto Save Function ===
def auto_save(result, save_path=output_json):
    """Append classification result with id, label, and text to a JSONL file."""
    with open(save_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(result) + "\n")


def rsponse_generation(prompt): 
    # Query GPT-4 for the next assistant response
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=prompt,
        temperature=1,
        max_tokens=2048
    )
    return response['choices'][0]['message']['content']


df = pd.read_csv(input_csv)

sample_3 = df[df['conversation_turns'] == 3].sample(2)
sample_5 = df[df['conversation_turns'] == 5].sample(2)
sample_7 = df[df['conversation_turns'] == 7].sample(2)

df = pd.concat([sample_3, sample_5, sample_7])
print(len(df))
processed_ids = set()

# Read existing JSONL file to avoid duplicates
if os.path.exists(output_json):
    with open(output_json, "r", encoding="utf-8") as f:
        for line in f:
            try:
                entry = json.loads(line)
                processed_ids.add(entry["prompt_id"])
            except:
                continue

# === Process and Save Results ===
for idx, row in tqdm(df.iterrows(), total=len(df)):
    print("idx = ", idx)
    print(row)
  
    prompt = row['prompt']
    prompt = ast.literal_eval(prompt)
    print(prompt)
    prompt_id = row['prompt_id']
    conversation_turns = row['conversation_turns']
    if prompt_id not in processed_ids:
        response = rsponse_generation(prompt)
        result = {
            "prompt_id": prompt_id,
            "conversation_turns": conversation_turns,
            "prompt": prompt,
            "response": response
        }
        auto_save(result)
        time.sleep(2)