# Models

This directory contains the trained machine-learning artifacts used by the Hotel Review Sentiment Intelligence application.

## Files

### `tfidf_vectorizer.joblib`

Trained TF-IDF vectorizer used to transform cleaned hotel review text into numerical features.

Configuration used during training:

- Maximum features: 5,000
- English stop-word removal
- Trained only on the training portion of the dataset

### `sentiment_model.joblib`

Trained Logistic Regression classifier used to predict:

- Positive
- Neutral
- Negative

The model was trained using TF-IDF features generated from cleaned hotel review text.

## Model Performance

Overall test accuracy:

**85.61%**

Performance differs across sentiment classes, with the model performing strongest on Positive reviews and weakest on Neutral reviews.

## Important

These model files should only be loaded from trusted sources because serialized model files can execute code when loaded.
