import streamlit as st
import pandas as pd

# ---------- PAGE HEADER ----------
st.markdown("<h1 style='color:#1E88E5; font-weight:700;'> Data Information & Feature Overview</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#555;'>Quick overview of the training and testing data, along with feature explanations.</p>", unsafe_allow_html=True)
st.write("---")

# ---------- LOAD DATA ----------
train_path = "pages/data/churn-bigml-80.csv"
test_path = "pages/data/churn-bigml-20.csv"

@st.cache_data
def load_data(train_path, test_path):
    train_df = pd.read_csv(train_path)
    test_df = pd.read_csv(test_path)
    merged = pd.concat([train_df, test_df], ignore_index=True)
    return train_df, test_df, merged

train_df, test_df, merged = load_data(train_path, test_path)

# ---------- BASIC INFO ----------
col1, col2, col3 = st.columns(3)
col1.metric("Train shape", f"{train_df.shape[0]} rows × {train_df.shape[1]} cols")
col2.metric("Test shape", f"{test_df.shape[0]} rows × {test_df.shape[1]} cols")
col3.metric("Total merged rows", f"{merged.shape[0]}")

st.write("---")

# ---------- PREVIEW ----------
st.subheader(" Data Preview")

col1, col2 = st.columns(2)
with col1:
    st.markdown("**Training Data (80%)**")
    st.dataframe(train_df.head(5), use_container_width=True)
with col2:
    st.markdown("**Testing Data (20%)**")
    st.dataframe(test_df.head(5), use_container_width=True)

st.info(f" Training dataset shape: {train_df.shape} | Testing dataset shape: {test_df.shape}")

st.write("---")

# ---------- COLUMN DEFINITIONS ----------
st.subheader(" Feature Definitions")

st.markdown("""
| Feature | Description |
|----------|-------------|
| `State` | U.S. state of the customer |
| `Account_length` | Days the customer has been with the company |
| `Area_code` | Telephone area code |
| `International_plan` | Whether the customer has an international plan (Yes/No) |
| `Voice_mail_plan` | Whether the customer has a voicemail plan (Yes/No) |
| `Number_vmail_messages` | Number of voice mail messages |
| `Total_day/eve/night_charge` | Call charges at different times of day |
| `Total_intl_*` | International minutes, calls, and charges |
| `Customer_service_calls` | Number of calls made to customer service |
| `Churn` | Target variable — 1 if customer left, 0 otherwise |
""")

st.write("---")

st.markdown("<p style='color:#777; font-size:15px;'>Tip: You can inspect the dataset further in the analysis section for detailed visuals and insights.</p>", unsafe_allow_html=True)
