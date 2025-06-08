## 📊 Ethiopian Mobile Banking App Review Analysis

This project analyzes customer satisfaction for mobile banking apps of three Ethiopian banks—**Commercial Bank of Ethiopia (CBE)**, **Bank of Abyssinia (BOA)**, and **Dashen Bank**—based on Google Play Store reviews. It simulates a real consulting project for Omega Consultancy.

---

### ✅ Task 1: Data Collection & Preprocessing

**Goals:**

- Scrape 400+ reviews from each bank's app (total: 1200+).
- Clean, deduplicate, and normalize the dataset.

**Steps:**

- Scraped using [`google-play-scraper`](https://github.com/digitalepidemiologylab/gplaycli).
- Removed duplicates and missing entries.
- Normalized review date to `YYYY-MM-DD` format.
- Stored final cleaned data in `cleaned_bank_reviews.csv`.

📁 **CSV Columns:**

- `review`, `rating`, `date`, `bank`, `source`

---

### ✅ Task 2: Sentiment & Thematic Analysis

**Sentiment Analysis**

- Used `distilbert-base-uncased-finetuned-sst-2-english` via Hugging Face.
- Labeled each review as: `positive`, `negative`, or `neutral`
- Saved sentiment output in `sentiment_reviews.csv`.

**Thematic Analysis**

- Preprocessed reviews using spaCy: lemmatization, stopword removal.
- Extracted keywords and bi-grams using TF-IDF.
- Grouped extracted keywords into 5 key themes:
  1. **Account Access Issues**
  2. **Transaction Performance**
  3. **UI/UX**
  4. **Customer Support**
  5. **Feature Requests**
- Saved output in `thematic_reviews.csv`

📁 **Output Columns:**

- `review`, `sentiment_label`, `sentiment_score`, `identified_themes`

---

### 🔧 Environment Setup

1. Clone this repo
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # or .\venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
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
