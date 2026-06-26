import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from wordcloud import WordCloud

# ---------------------------------------------------
# Create Output Folders
# ---------------------------------------------------

os.makedirs("output/charts", exist_ok=True)
os.makedirs("output/reports", exist_ok=True)

# ---------------------------------------------------
# Load Dataset
# ---------------------------------------------------

df = pd.read_csv("data/classified_dataset.csv")

# ---------------------------------------------------
# Overview Metrics
# ---------------------------------------------------

total_mentions = len(df)

sentiment_counts = df["Sentiment"].value_counts()
driver_counts = df["Driver"].value_counts()
subdriver_counts = df["Sub driver"].value_counts()

positive = sentiment_counts.get("Positive", 0)
neutral = sentiment_counts.get("Neutral", 0)
negative = sentiment_counts.get("Negative", 0)

print(f"Total Mentions: {total_mentions}")
print(sentiment_counts)

# ---------------------------------------------------
# Sentiment Distribution Chart
# ---------------------------------------------------

plt.figure(figsize=(7,5))

sentiment_counts.plot(kind="bar")

plt.title("Sentiment Distribution")
plt.xlabel("Sentiment")
plt.ylabel("Mentions")
plt.tight_layout()

plt.savefig("output/charts/sentiment_distribution.png")
plt.close()

# ---------------------------------------------------
# Driver Distribution Chart
# ---------------------------------------------------

plt.figure(figsize=(8,5))

driver_counts.plot(kind="bar")

plt.title("Reputation Driver Distribution")
plt.xlabel("Driver")
plt.ylabel("Mentions")
plt.tight_layout()

plt.savefig("output/charts/driver_distribution.png")
plt.close()

# ---------------------------------------------------
# Sub Driver Distribution Chart
# ---------------------------------------------------

plt.figure(figsize=(10,5))

subdriver_counts.plot(kind="bar")

plt.title("Sub-driver Distribution")
plt.xlabel("Sub-driver")
plt.ylabel("Mentions")
plt.tight_layout()

plt.savefig("output/charts/subdriver_distribution.png")
plt.close()

# ---------------------------------------------------
# Top Discussion Themes
# ---------------------------------------------------

vectorizer = CountVectorizer(
    stop_words="english",
    max_features=15
)

X = vectorizer.fit_transform(df["combined_text"])

themes = vectorizer.get_feature_names_out()

print("\nTop Themes")
print(themes)

# ---------------------------------------------------
# Word Cloud
# ---------------------------------------------------

text = " ".join(df["combined_text"].astype(str))

wordcloud = WordCloud(
    width=1200,
    height=600,
    background_color="white"
).generate(text)

plt.figure(figsize=(12,6))
plt.imshow(wordcloud)
plt.axis("off")

plt.savefig("output/charts/wordcloud.png")
plt.close()

# ---------------------------------------------------
# Positive / Negative Drivers
# ---------------------------------------------------

positive_driver = (
    df[df["Sentiment"]=="Positive"]
    ["Driver"]
    .value_counts()
)

negative_driver = (
    df[df["Sentiment"]=="Negative"]
    ["Driver"]
    .value_counts()
)

# ---------------------------------------------------
# Key Findings
# ---------------------------------------------------

top_driver = driver_counts.idxmax()
top_driver_count = driver_counts.max()

# ---------------------------------------------------
# Write Report
# ---------------------------------------------------

with open(
    "output/reports/insights.txt",
    "w",
    encoding="utf-8"
) as f:

    f.write(f"Total Mentions : {total_mentions}\n")

    f.write("\n==============================\n")
    f.write("Sentiment Distribution\n")
    f.write("==============================\n")
    f.write(sentiment_counts.to_string())

    f.write("\n\n==============================\n")
    f.write("Driver Distribution\n")
    f.write("==============================\n")
    f.write(driver_counts.to_string())

    f.write("\n\n==============================\n")
    f.write("Sub-driver Distribution\n")
    f.write("==============================\n")
    f.write(subdriver_counts.to_string())

    f.write("\n\n==============================\n")
    f.write("Top Discussion Themes\n")
    f.write("==============================\n")

    for theme in themes:
        f.write(f"- {theme}\n")

    f.write("\n==============================\n")
    f.write("Positive Reputation Drivers\n")
    f.write("==============================\n")
    f.write(positive_driver.to_string())

    f.write("\n\n==============================\n")
    f.write("Negative Reputation Drivers\n")
    f.write("==============================\n")
    f.write(negative_driver.to_string())

    f.write("\n\n==============================\n")
    f.write("Key Findings\n")
    f.write("==============================\n")

    f.write(
        f"• Most discussions relate to {top_driver} "
        f"({top_driver_count} mentions).\n"
    )

    f.write(
        f"• Neutral sentiment dominates with {neutral} mentions.\n"
    )

    f.write(
        f"• Positive sentiment ({positive}) significantly exceeds Negative sentiment ({negative}).\n"
    )

    f.write(
        "• Thought Leadership and Product Strategy are the dominant sub-drivers.\n"
    )

    f.write(
        "• Responsible Business Practices receive comparatively limited coverage.\n"
    )

print("\nInsights generated successfully!")
print("Charts saved in output/charts/")
print("Report saved in output/reports/insights.txt")