# Data

This directory documents the dataset used in the Hotel Review Sentiment Intelligence project.

## Dataset

**TripAdvisor Hotel Reviews**

- 20,491 hotel guest reviews
- Review text
- Guest rating from 1 to 5
- Used for sentiment classification and complaint-theme analysis

The analytical notebook expects the dataset locally at:

`data/tripadvisor_hotel_reviews.csv`

## Sentiment Labels

Guest ratings were converted into three sentiment classes:

- **1–2:** Negative
- **3:** Neutral
- **4–5:** Positive

## Usage

The raw dataset is used for:

- exploratory review analysis
- text preprocessing
- sentiment label creation
- TF-IDF feature extraction
- Logistic Regression training
- complaint-theme analysis

The dataset itself may be obtained from the original TripAdvisor Hotel Reviews source on Kaggle.
