import streamlit as st

st.set_page_config(page_title="About Project & Steps", layout="wide")

st.title(" About Project & Steps")
st.markdown("---")

st.markdown("""
### **Project Overview**
A **Telecom Customer Churn Prediction System** built using **Data Science & Machine Learning**  
to identify customers who are likely to leave the company and reveal the key factors behind churn.
""")

st.markdown("---")

st.markdown("""
            
### **Project Cycle (Summary)**

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

""")

st.markdown("---")



st.markdown("""
### **Tools & Technologies**
- **Python**, **Pandas**, **NumPy**, **Scikit-learn**, **Plotly**, **Streamlit**  
- Machine Learning Algorithms: Random Forest, GridSearchCV  
- Deployed using Streamlit for **interactive prediction & analysis**
""")
