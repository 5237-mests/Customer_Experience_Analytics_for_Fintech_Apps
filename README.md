# Mobile Banking App Reviews Analysis

## Overview

This project analyzes user feedback from the Google Play Store for mobile apps from:

- Commercial Bank of Ethiopia
- Bank of Abyssinia
- Dashen Bank

## Task 1: Data Collection

- Used `google-play-scraper` to extract 400+ reviews per app.
- Removed duplicates, formatted dates, and saved a clean CSV file.

## Files

- `scraper.py`: Extracts raw reviews.
- `preprocess.py`: Cleans and formats the dataset.
- `cleaned_bank_reviews.csv`: Final dataset.
