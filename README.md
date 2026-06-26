# 🏦 AI Reputation Intelligence Dashboard

> **AI & Data Solutions Specialist Assignment**
> AI-powered Digital Reputation Analysis for **ICICI Prudential AMC**

![Python](https://img.shields.io/badge/Python-3.13-blue?style=flat-square)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red?style=flat-square)
![Plotly](https://img.shields.io/badge/Plotly-Interactive-blueviolet?style=flat-square)
![Mistral AI](https://img.shields.io/badge/Mistral-AI-orange?style=flat-square)

---

## 📌 Overview

This project implements an end-to-end **AI-powered Reputation Intelligence System** that transforms raw media mentions into actionable business insights.

The solution includes:

* Data preprocessing
* AI-powered classification using Mistral AI
* Reputation analytics
* Interactive Streamlit dashboard
* Executive business insights

---

## 🎯 Objectives

* Clean and preprocess raw media data
* Classify reputation drivers using AI
* Generate business insights
* Visualize reputation trends
* Build an interactive dashboard

---

## 🏗️ Solution Workflow

```text
Raw Dataset
     │
     ▼
Data Cleaning
     │
     ▼
Text Preprocessing
     │
     ▼
AI Classification (Mistral AI)
     │
     ▼
Insight Generation
     │
     ▼
Interactive Dashboard
```

---

## 📂 Project Structure

```text
eminence-assignment/
│
├── dashboard/
│   └── app.py
│
├── data/
│   ├── Dataset.xlsx
│   ├── cleaned_dataset.csv
│   └── classified_dataset.csv
│
├── docs/
│   ├── Methodology.pdf
│   └── Scalability_Approach.pdf
│
├── output/
│   ├── charts/
│   └── reports/
│
├── src/
│   ├── preprocess.py
│   ├── classifier.py
│   ├── insights.py
│   ├── prompts.py
│   └── taxonomy.py
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Project Phases

### Phase 1 — Data Exploration

* Dataset profiling
* Missing value analysis
* Duplicate detection
* Exploratory statistics

### Phase 2 — Data Preprocessing

Performed:

* Duplicate removal
* Missing value handling
* Text normalization
* Source normalization
* Sentiment standardization
* Combined text generation

**Output**

`data/cleaned_dataset.csv`

---

### Phase 3 — AI Classification

The classification pipeline uses **Mistral AI** to classify each article into:

#### Reputation Drivers

* Brand Perception
* User Experience
* Responsible Business Practices

#### Reputation Sub-drivers

* Thought Leadership
* Product Strategy
* Brand Visibility & Marketing
* Product & Service Quality
* Customer Support & Complaint Resolution
* Digital & Omnichannel Experience
* Regulatory Compliance & Ethical Governance
* Social Impact & Community (CSR)

**Output**

`data/classified_dataset.csv`

---

### Phase 4 — Insight Generation

Automatically generates:

* Total Mentions
* Sentiment Distribution
* Driver Distribution
* Sub-driver Distribution
* Top Discussion Themes
* Positive Drivers
* Negative Drivers
* Word Cloud
* Executive Summary

---

### Phase 5 — Interactive Dashboard

#### 📊 Overview

* KPI Cards
* Sentiment Distribution
* Driver Distribution
* Sub-driver Distribution
* Word Cloud
* Discussion Themes

#### 🔍 Content Explorer

* Search Articles
* Filter by Driver
* Filter by Sub-driver
* Filter by Sentiment
* Original Content Viewer
* Download Filtered Data

#### 🧠 AI Insights

* Positive Drivers
* Negative Drivers
* Executive Summary
* Business Recommendations
* Key Findings

---

## 💻 Technology Stack

| Category         | Technologies                  |
| ---------------- | ----------------------------- |
| Programming      | Python 3.13                   |
| Data Processing  | Pandas, NumPy                 |
| AI               | Mistral AI                    |
| Visualization    | Plotly, Matplotlib, WordCloud |
| Machine Learning | Scikit-learn                  |
| Dashboard        | Streamlit                     |

---

## 🚀 Installation

Clone the repository

```bash
git clone <repository-url>
cd eminence-assignment
```

Create virtual environment

```bash
python -m venv venv
```

Activate virtual environment

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create a `.env` file.

```env
MISTRAL_API_KEY=your_api_key_here
```

---

## ▶️ Run the Project

### 1. Data Cleaning

```bash
python src/preprocess.py
```

### 2. AI Classification

```bash
python src/classifier.py
```

### 3. Generate Insights

```bash
python src/insights.py
```

### 4. Launch Dashboard

```bash
streamlit run dashboard/app.py
```

---

## 📊 Dashboard Features

* Interactive KPI Cards
* Sentiment Analytics
* Driver Analytics
* Sub-driver Analytics
* Word Cloud
* Discussion Themes
* Interactive Search
* Article Explorer
* Download Filtered CSV
* Executive Insights

---

## 📈 Outputs

The application generates:

* Cleaned Dataset
* Classified Dataset
* Sentiment Distribution Chart
* Driver Distribution Chart
* Sub-driver Distribution Chart
* Word Cloud
* Insights Report
* Interactive Dashboard

---

## ⚠️ Assumptions

* The provided dataset is representative of digital reputation mentions.
* Existing sentiment labels are used as provided.
* Mistral AI classifies only Driver and Sub-driver categories.

---

## 🚀 Future Enhancements

* Real-time News API integration
* Reddit integration
* X (Twitter) integration
* Automated ETL pipelines
* PostgreSQL / MongoDB storage
* Topic Modeling
* Trend Detection
* Multi-brand comparison
* AI-generated daily executive reports

---

## 👨‍💻 Author

**Dheeraj Chaubey**

AI & Data Solutions Specialist Assignment

---

## 📄 License

This project was developed exclusively for the **AI & Data Solutions Specialist Assignment** and is intended for evaluation purposes only.
