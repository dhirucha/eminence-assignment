import pandas as pd

# Load dataset
df = pd.read_excel("data/Dataset.xlsx")

# -------------------------------
# Remove duplicate rows
# -------------------------------
before = len(df)

df = df.drop_duplicates()

after = len(df)

print(f"Removed {before-after} duplicate rows")

# -------------------------------
# Standardize sentiment
# -------------------------------
df["Sentiment"] = (
    df["Sentiment"]
    .astype(str)
    .str.strip()
    .str.capitalize()
)

# -------------------------------
# Fill missing text columns
# -------------------------------
text_columns = [
    "Title",
    "Opening Text",
    "Hit Sentence",
    "Source Name"
]

for col in text_columns:
    df[col] = df[col].fillna("")

# -------------------------------
# Create combined text
# -------------------------------
df["combined_text"] = (
    df["Title"] + " " +
    df["Opening Text"] + " " +
    df["Hit Sentence"]
)

df["combined_text"] = (
    df["combined_text"]
    .str.replace(r"\s+", " ", regex=True)
    .str.strip()
)

# -------------------------------
# Calculate text length
# -------------------------------
df["text_length"] = df["combined_text"].str.len()

# -------------------------------
# Remove only completely empty rows
# -------------------------------
df = df[
    df["combined_text"].str.strip() != ""
]

# -------------------------------
# Standardize Source Name
# -------------------------------
df["Source Name"] = (
    df["Source Name"]
    .str.strip()
    .str.title()
)

# -------------------------------
# Save cleaned dataset
# -------------------------------
df.to_csv(
    "data/cleaned_dataset.csv",
    index=False
)

# -------------------------------
# Cleaning report
# -------------------------------
report = f"""
Records after cleaning: {len(df)}

Duplicate rows removed

Sentiment standardized

Missing text handled

Combined text created

Dataset ready for AI classification
"""

with open(
    "output/cleaning_report.txt",
    "w",
    encoding="utf-8"
) as f:
    f.write(report)

# -------------------------------
# Summary
# -------------------------------
print(df.isnull().sum())

print(df["text_length"].describe())

print(f"Final Records: {len(df)}")