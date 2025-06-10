# 📊 Ethiopian Mobile Banking App Review Analysis

This project analyzes customer satisfaction for mobile banking apps of three Ethiopian banks—**Commercial Bank of Ethiopia (CBE)**, **Bank of Abyssinia (BOA)**, and **Dashen Bank**—based on Google Play Store reviews. It simulates a real consulting project for Omega Consultancy.

---

## ✅ Task 1: Data Collection & Preprocessing

### Goals:

- Scrape 400+ reviews from each bank's app (total: 1200+).
- Clean, deduplicate, and normalize the dataset.

### Steps:

- Scraped using [`google-play-scraper`](https://github.com/digitalepidemiologylab/gplaycli).
- Removed duplicates and missing entries.
- Normalized review dates to `YYYY-MM-DD` format.
- Stored final cleaned data in `cleaned_bank_reviews.csv`.

### 📁 CSV Columns:

- `review`, `rating`, `date`, `bank`, `source`

---

## ✅ Task 2: Sentiment & Thematic Analysis

### Sentiment Analysis:

- Used `distilbert-base-uncased-finetuned-sst-2-english` from Hugging Face.
- Also applied VADER for comparison and validation.
- Labeled reviews as: `positive`, `negative`, or `neutral`.
- Saved results in `sentiment_reviews.csv`.

### Thematic Analysis:

- Preprocessed text using spaCy: tokenization, stopword removal, lemmatization.
- Extracted keywords and bi-grams using TF-IDF and CountVectorizer.
- Defined and grouped into five main themes:
  1. **Account Access Issues**
  2. **Transaction Performance**
  3. **UI/UX**
  4. **Customer Support**
  5. **Feature Requests**

### 📁 Output Columns:

- `review`, `sentiment_label`, `sentiment_score`, `identified_themes`

---

## ✅ Task 3: Keyword & Theme Grouping

### Approach:

- Grouped semantically similar keywords into themes using TF-IDF + domain knowledge.
- Created a manual mapping of keywords to themes using curated dictionaries.
- Stored enhanced data in `theme_mapped_reviews.csv`.

---

## ✅ Task 4: Insights & Recommendations

### Key Insights:

- **Dashen Bank**: Positive UI/UX feedback but recurring transaction failures.
- **CBE**: Most negative reviews tied to login and access issues.
- **BOA**: Appreciated for simplicity but users reported lag and poor response.

### Visualizations:

- Sentiment distribution per bank.
- Monthly sentiment trend lines.
- Bar charts of most common complaint themes.
- Word clouds per sentiment category.

> 📍 All plots are available in `notebooks/task_4_analysis.ipynb`.

### Recommendations:

- Implement crash/error reporting inside apps.
- Prioritize login reliability and session stability.
- Add modern features like personal finance tracking (BOA, CBE).
- Improve customer support responsiveness via live chat or in-app tickets.

### Ethical Considerations:

- Reviews can be biased by personal emotions or temporary bugs.
- Regional languages (e.g., Amharic, Afan Oromo) may be underrepresented.

---

## 🔧 Environment Setup

1. Clone this repo:
   ```bash
   git clone https://github.com/5237-mests/Customer_Experience_Analytics_for_Fintech_Apps.git
   cd Customer_Experience_Analytics_for_Fintech_Apps
   ```

---

### 📂 Directory Structure

```
CUSTOMER_EXPERIENCE_ANALYTICS_FOR_FINTECH_APPS/
├── .git
├── .github/
│   └── workflows/
├── data/
├── notebooks/
│   ├── __init__.py
│   ├── preprocess.ipynb
│   └── scraper.ipynb
├── scripts/
│   ├── __init__.py
│   └── README.md
├── src/
│   └── __init__.py
├── tests/
│   └── __init__.py
├── .gitignore
├── README.md
└── requirements.txt
```
