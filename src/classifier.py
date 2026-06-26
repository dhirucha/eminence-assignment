import os
import json
import re
import time
import pandas as pd

from dotenv import load_dotenv
from mistralai.client import Mistral
from prompts import CLASSIFICATION_PROMPT

# --------------------------------------------------
# Load Environment Variables
# --------------------------------------------------

load_dotenv()

api_key = os.getenv("MISTRAL_API_KEY")

if not api_key:
    raise ValueError("MISTRAL_API_KEY not found in .env")

client = Mistral(api_key=api_key)

# --------------------------------------------------
# Classification Function
# --------------------------------------------------

def classify_article(text):

    if not text.strip():
        return {
            "driver": "Unknown",
            "sub_driver": "Unknown"
        }

    prompt = CLASSIFICATION_PROMPT.format(text=text)

    retries = 3

    for attempt in range(retries):

        try:

            response = client.chat.complete(
                model="mistral-small-latest",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            output = response.choices[0].message.content.strip()

            # Extract JSON only
            match = re.search(r"\{.*\}", output, re.DOTALL)

            if not match:
                raise ValueError(f"No JSON found:\n{output}")

            return json.loads(match.group())

        except Exception as e:

            print(f"Attempt {attempt+1} failed: {e}")

            time.sleep(3)

    # If all retries fail
    return {
        "driver": "Unknown",
        "sub_driver": "Unknown"
    }


# --------------------------------------------------
# Load Dataset
# --------------------------------------------------

df = pd.read_csv("data/cleaned_dataset.csv")

drivers = []
subdrivers = []

total = len(df)

print(f"\nStarting classification of {total} records...\n")

# --------------------------------------------------
# Classification Loop
# --------------------------------------------------

for i, article in enumerate(df["combined_text"], start=1):

    print(f"[{i}/{total}] Processing...")

    result = classify_article(article)

    drivers.append(result["driver"])
    subdrivers.append(result["sub_driver"])

    # Backup every 10 records
    if i % 10 == 0:

        temp_df = df.iloc[:i].copy()

        temp_df["Driver"] = drivers
        temp_df["Sub driver"] = subdrivers

        temp_df.to_csv(
            "data/classified_dataset_backup.csv",
            index=False
        )

        print(f" Backup saved ({i} records)\n")

# --------------------------------------------------
# Save Final Dataset
# --------------------------------------------------

df["Driver"] = drivers
df["Sub driver"] = subdrivers

unknown = df[df["Driver"]=="Unknown"]

print(
    unknown[
        ["Title","combined_text"]
    ]
)

df.to_csv(
    "data/classified_dataset.csv",
    index=False
)

print("\n Classification Completed Successfully!")
print("Saved to data/classified_dataset.csv")