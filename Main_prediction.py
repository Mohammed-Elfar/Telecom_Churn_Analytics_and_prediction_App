import streamlit as st
import pandas as pd
import joblib

# ========== PAGE CONFIG ==========
st.set_page_config(page_title="Telecom Churn Prediction", layout="wide")
st.title(" TELECOM CUSTOMER CHURN PREDICTION APP")

MODEL_PATH = "/Users/mohammedmahmood/Desktop/Telecom_Churn_App/model/Telecome_Churn_Prediction.joblib"

# Load trained model
model = joblib.load(MODEL_PATH)

st.markdown("Use this page to predict whether a telecom customer will **churn or stay** based on their details.")

# ========== INPUT SECTION ==========
col1, col2 = st.columns(2)
with col1:
    international_plan = st.selectbox("International Plan", ["No", "Yes"])
    voice_mail_plan = st.selectbox("Voice Mail Plan", ["No", "Yes"])
    account_length = st.slider("Account Length", 1, 243, 120)
    number_vmail_messages = st.slider("Number of Voice Mail Messages", 0, 51, 10)
with col2:
    total_day_charge = st.slider("Total Day Charge", 0.0, 59.64, 30.56)
    total_eve_charge = st.slider("Total Evening Charge", 0.0, 30.91, 17.08)
    total_night_charge = st.slider("Total Night Charge", 1.04, 17.77, 9.04)
    total_intl_minutes = st.slider("Total International Minutes", 0.0, 20.0, 10.0)
    total_intl_calls = st.slider("Total International Calls", 0, 20, 4)
    total_intl_charge = st.slider("Total International Charge", 0.0, 5.4, 2.76)

Total_charge = total_day_charge + total_eve_charge + total_night_charge
st.metric("Total Charge (Auto Calculated)", f"{Total_charge:.2f}")

customer_service_calls = st.slider("Customer Service Calls", 0, 9, 1)
high_service_calls = int(customer_service_calls > 3)
if high_service_calls:
    st.error("🚨 High number of service calls")
else:
    st.success("✅ Normal number of service calls")

# ========== PREPARE INPUT DATA ==========
input_data = pd.DataFrame([{
    'Account_length': account_length,
    'International_plan': international_plan,
    'Voice_mail_plan': voice_mail_plan,
    'Number_vmail_messages': number_vmail_messages,
    'Total_day_charge': total_day_charge,
    'Total_eve_charge': total_eve_charge,
    'Total_night_charge': total_night_charge,
    'Total_intl_minutes': total_intl_minutes,
    'Total_intl_calls': total_intl_calls,
    'Total_intl_charge': total_intl_charge,
    'Customer_service_calls': customer_service_calls,
    'High_service_calls': high_service_calls,
    'Total_charge': Total_charge,
}])

# ========== PREDICTION ==========
if st.button("Predict Churn of Coustomer"):
    prediction = model.predict(input_data)[0]
    proba = model.predict_proba(input_data)[0][1]

    st.subheader("Prediction Result:")
    if prediction == 1:
        st.error(f"🔻 This customer is **likely to CHURN** with probability {proba:.2%}")
    else:
        st.success(f"🟢 This customer is **likely to STAY** with probability {proba:.2%}")
