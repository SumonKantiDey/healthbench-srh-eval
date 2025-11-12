import openai
import json
import pandas as pd
import os
from tqdm import tqdm
import time 
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("myna_openai")

openai.api_key = API_KEY

# === Input and Output Settings ===
input_csv = "./data/health_bench_crafted.csv"                         # Input file
text_column = "prompt"                                # Column name with the text
output_json = "./data/srh_classification_results.jsonl"    # Output JSONL file

# === Auto Save Function ===
def auto_save(result, save_path=output_json):
    """Append classification result with id, label, and text to a JSONL file."""
    with open(save_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(result) + "\n")

# === SRH Classification Function ===
def classify_srh(text):
    """Use GPT-4 to classify the input text as SRH-related or not."""
    prompt = f"""Determine whether the following text is related to Sexual and Reproductive Health (SRH).
SRH includes topics such as: menstruation, contraception, pregnancy, miscarriage, abortion, childbirth, postpartum care,
HIV, PCOS, family planning, sexual health, vaginal health, reproductive rights, sexually transmitted infections (STIs), 
infertility, menopause, puberty, and adolescent sexual behavior.

Respond with one of the following labels:
- SRH-Related
- Not SRH-Related

Text: {text}
Answer:"""

    try:
        print(prompt)
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a public health expert."},
                {"role": "user", "content": prompt}
            ],
            temperature=0,
            max_tokens=10
        )
        label = response['choices'][0]['message']['content'].strip()
        return label

    except Exception as e:
        print(f"❌ Error: {e}")
        return "Error"

# === Load CSV and Track Already Processed IDs ===
df = pd.read_csv(input_csv)
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
    text = str(row[text_column]).strip()
    prompt_id = row['prompt_id']
    if prompt_id not in processed_ids and text:
        label = classify_srh(text)
        result = {
            "prompt_id": prompt_id,
            "label": label,
            "prompt": text
        }
        auto_save(result)
        time.sleep(2)