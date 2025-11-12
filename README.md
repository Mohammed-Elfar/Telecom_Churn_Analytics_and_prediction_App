# Telecom Churn Prediction

The goal is to predict whether a telecom customer will churn (stop using the service) based on features like usage patterns, account details, and customer service interactions. 

**link of the app** : https://telecomchurnapp-bcn7eihwj9yz9dws8r57w2.streamlit.app/

## **Project Cycle:**

1. **Check data quality (Missing & Duplicates)** - Reviewed data types, and verify if it is correct. Also check for missing & duplicate values.

2. **Univariate analysis** — In this step, I went through each column individually to identify and address any issues, and performed EDA to gain a deeper understanding of the features.

3. **Bivariate analysis** — Explored the relationship between each feature and the target variable (Churn) to discover useful patterns.

4. **Multivariate analysis** — Analyzed how multiple features interact together and how they collectively affect churn.

5. **Feature extraction** — Created new features from existing ones to improve the model’s learning capability and overall performance.

6. **Feature importance** — Used correlation and ExtraTreesClassifier to identify the most important features for the model, and removed less impactful ones.

7. **ML Pipelines** —Built separate pipelines for categorical and numerical data to handle missing values, encoding, scaling, and class imbalance automatically — ensuring a clean, repeatable workflow.

8. **Model training** — Trained several machine learning models using cross-validation and pipelines to prevent data leakage and evaluate consistent performance.

9. **Choose best model** — Selected **Random Forest** as the best model based on performance metrics.

10. **Tuning** — Optimized the Random Forest hyperparameters using **GridSearchCV**, achieving **98% accuracy, 85% recall, and 98% precision**.

11. **Deployment** — Deployed the final model using **Streamlit** for real-time churn prediction.


