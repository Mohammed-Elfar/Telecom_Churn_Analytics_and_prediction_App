##### Note
**Interactive notebook & full analysis (plots + code) are hosted on Kaggle.**  
Open the live Kaggle notebook to see interactive Plotly charts and run cells:

🔗 **Kaggle Notebook (interactive):**  
https://www.kaggle.com/code/mohammadelfar/telecome-churn-prediction-97-acc-97-precision


# Telecom Churn Prediction 

**This application is an end-to-end Streamlit project for predicting customer churn in a telecom company.
It includes real-time prediction, full data exploration, feature explanations, and insights to support business decisions.**

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


## App Structure

## 1. **Prediction Tab**
Provides real-time churn predictions for new customers.
Users enter customer information and receive a churn prediction with probability.

## 2. **Data Info & Feature Explanation Tab**
Includes:
- Dataset structure
- Column descriptions
- Feature definitions

## 3. **Analysis & Insights Tab**
Displays:
- Bivariate and multivariate analysis
- Visual trends explaining churn behavior
- Business recommendations

## 4. **About Project & Steps Tab**
Summarizes the entire workflow:
- Data exploration
- Cleaning and feature engineering
- Model training and evaluation
- Deployment using Streamlit

---

## Key Insights and Recommendations

## 1. **International Plan Users Have High Churn**
Customers with an International Plan show a churn rate of about 42%.
**Recommendation:** Review pricing and improve service quality.

## 2. **High Number of Customer Service Calls Predicts Churn**
Customers making three or more customer service calls are highly likely to churn.
**Recommendation:** Flag these customers early for proactive retention.

## 3. **Voice Mail Plan Reduces Churn**
Voice Mail Plan users have significantly lower churn.
**Recommendation:** Promote service bundles and upsell optional plans.

## 4. **Long-Term Customers Without Extra Plans Still Churn**
Long-tenure customers without additional services still show churn risk.
**Recommendation:** Offer loyalty programs and retention incentives.
"""

