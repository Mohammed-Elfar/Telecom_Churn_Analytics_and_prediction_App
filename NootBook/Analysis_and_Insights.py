# pages/2_Analysis_and_Insights.py
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Analysis & Insights", layout="wide")
st.markdown("<h2 style='color:#1E88E5;'>📈 Analysis & Insights</h2>", unsafe_allow_html=True)

@st.cache_data(ttl=3600)
def load_data(path="data/churn-bigml-80.csv"):
    df = pd.read_csv(path)
    return df

# --- load dataset (allow override by upload) ---
uploaded = st.file_uploader("Upload CSV (optional) — overrides default dataset", type=["csv"])
if uploaded is not None:
    df = pd.read_csv(uploaded)
    st.success("Uploaded dataset loaded.")
else:
    try:
        df = load_data()
    except Exception as e:
        st.error(f"Could not load default dataset: {e}")
        st.stop()

# --- helper: normalize churn to numeric 0/1 and create Tenure_Bucket if missing ---
def prepare_df(df):
    df = df.copy()
    # normalize column names (strip)
    df.columns = [c.strip() for c in df.columns]
    # find churn column (case-insensitive)
    churn_col = next((c for c in df.columns if c.lower() == "churn"), None)
    if churn_col is None:
        st.error("No 'Churn' column found (case-insensitive). Please ensure your dataset has a 'Churn' column.")
        st.stop()
    # create numeric churn if needed
    if df[churn_col].dtype == object:
        df["_churn_num"] = df[churn_col].apply(lambda x: 1 if str(x).strip().lower() in ("yes","y","true","1") else 0)
    else:
        df["_churn_num"] = pd.to_numeric(df[churn_col], errors="coerce").fillna(0).astype(int)
    # account_length
    acct_col = next((c for c in df.columns if c.lower() in ("account_length","account length")), None)
    if acct_col is not None:
        if "Tenure_Bucket" not in df.columns:
            max_val = int(df[acct_col].max())
            bins = [0, 50, 150, max_val + 1]
            labels = ["New", "Mid", "Long"]
            df["Tenure_Bucket"] = pd.cut(df[acct_col], bins=bins, labels=labels)
    return df, churn_col

df, churn_col = prepare_df(df)

# --- Sidebar controls ---
st.sidebar.header("Chart controls")
chart_choice = st.sidebar.selectbox(
    "Select analysis chart",
    [
        "State churn (top states)",
        "Account length vs Churn (box)",
        "Churn by International Plan",
        "Churn by Voice Mail Plan",
        "Churn vs Customer Service Calls (line)",
        "Churn by Service Calls split by Intl Plan",
        "Intl charges vs churn (intl users box)",
        "Churn by Tenure Bucket & Intl Plan",
        "Churn by Tenure Bucket & Voice Mail Plan"
    ]
)

top_n = st.sidebar.slider("Top N (states)", 5, 50, 20, 5)

st.markdown("### Data preview")
st.dataframe(df.head(8))

st.markdown("---")

# --- chart implementations and insight text ---
if chart_choice == "State churn (top states)":
    # Use count of churn events or sum of numeric churn depending on data (user used count in notebook)
    # We'll show both: churn count (sum) and churn frequency later
    if "State" not in df.columns:
        st.warning("No 'State' column found in dataset.")
    else:
        # compute churn count by state (sum of _churn_num)
        state_churn = df.groupby("State")["_churn_num"].sum().reset_index().rename(columns={"_churn_num":"Churn_Count"})
        state_churn = state_churn.sort_values("Churn_Count", ascending=False).head(top_n)
        fig = px.bar(state_churn, x="State", y="Churn_Count",
                     title=f"Top {top_n} States by Churn (count)",
                     labels={"Churn_Count":"Churn Count"})
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("**Insight:** The states shown above have the highest churn counts. Consider regional retention campaigns for these areas.")
        st.markdown("**Recommendation:** Investigate localized reasons (pricing, coverage, service quality) and offer targeted retention offers.")

elif chart_choice == "Account length vs Churn (box)":
    acct_col = next((c for c in df.columns if c.lower() in ("account_length","account length")), None)
    if acct_col is None:
        st.warning("No account length column found. Expected 'Account_length'.")
    else:
        fig = px.box(df, x=df[churn_col], y=df[acct_col],
                     title="Account Length vs Churn",
                     labels={churn_col: "Churn (original)", acct_col: "Account Length (days)"})
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("**Insight:** Account length looks similar for churners and non-churners in many cases — tenure alone may not explain churn.")

elif chart_choice == "Churn by International Plan":
    col = next((c for c in df.columns if c.lower() == "international_plan"), None)
    if col is None:
        st.warning("No 'International_plan' column found.")
    else:
        intl_churn = df.groupby(col)["_churn_num"].mean().reset_index().rename(columns={"_churn_num":"Churn_Rate"})
        fig = px.bar(intl_churn, x=col, y="Churn_Rate", title="Churn Rate by International Plan", labels={"Churn_Rate":"Churn Rate"})
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("**Insight:** Customers with an International Plan churn much more compared to those without.")
        st.markdown("**Recommendation:** Focus on competitive pricing, improved support, or loyalty perks for international customers.")

elif chart_choice == "Churn by Voice Mail Plan":
    col = next((c for c in df.columns if c.lower() == "voice_mail_plan"), None)
    if col is None:
        st.warning("No 'Voice_mail_plan' column found.")
    else:
        vm_churn = df.groupby(col)["_churn_num"].mean().reset_index().rename(columns={"_churn_num":"Churn_Rate"})
        fig = px.bar(vm_churn, x=col, y="Churn_Rate", title="Churn Rate by Voice Mail Plan", labels={"Churn_Rate":"Churn Rate"})
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("**Insight:** Customers with a Voice Mail Plan churn less compared to those without. Extra services appear to increase loyalty.")
        st.markdown("**Recommendation:** Promote voicemail or bundle services to reduce churn.")

elif chart_choice == "Churn vs Customer Service Calls (line)":
    calls_col = next((c for c in df.columns if c.lower() in ("customer_service_calls","customer service calls")), None)
    if calls_col is None:
        st.warning("No 'Customer_service_calls' column found.")
    else:
        service_churn = df.groupby(calls_col)["_churn_num"].mean().reset_index().rename(columns={"_churn_num":"Churn_Rate"})
        fig = px.line(service_churn, x=calls_col, y="Churn_Rate", markers=True, title="Churn Rate vs Number of Customer Service Calls", labels={"Churn_Rate":"Churn Rate", calls_col:"Customer Service Calls"})
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("**Insight:** Churn rate stays low for 0–2 calls but jumps after 3+ calls, reaching very high values for many calls.")
        st.markdown("**Recommendation:** Flag customers with >3 service calls as high-risk and prioritize retention efforts.")

elif chart_choice == "Churn by Service Calls split by Intl Plan":
    calls_col = next((c for c in df.columns if c.lower() in ("customer_service_calls","customer service calls")), None)
    intl_col = next((c for c in df.columns if c.lower() == "international_plan"), None)
    if calls_col is None or intl_col is None:
        st.warning("Columns required ('Customer_service_calls' and 'International_plan') not found.")
    else:
        interaction = df.groupby([intl_col, calls_col])["_churn_num"].mean().reset_index()
        fig = px.line(interaction, x=calls_col, y="_churn_num", color=intl_col, markers=True,
                      title="Churn by Service Calls (split by International Plan)", labels={"_churn_num":"Churn Rate", calls_col:"Customer Service Calls"})
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("**Insight:** For international-plan customers, churn is higher and rises faster with more service calls.")
        st.markdown("**Recommendation:** Premium customers with many service calls should receive priority handling and special retention offers.")

elif chart_choice == "Intl charges vs churn (intl users box)":
    intl_col = next((c for c in df.columns if c.lower() == "international_plan"), None)
    if intl_col is None:
        st.warning("No 'International_plan' column found.")
    else:
        intl_users = df[df[intl_col].astype(str).str.lower() == "yes"]
        if intl_users.shape[0] == 0:
            st.warning("No international-plan users with 'Yes' found in dataset.")
        else:
            # find total intl charge column
            intl_charge_col = next((c for c in df.columns if c.lower() in ("total_intl_charge","total intl charge")), None)
            if intl_charge_col is None:
                st.warning("No 'Total_intl_charge' column found.")
            else:
                fig = px.box(intl_users, x=intl_users[churn_col], y=intl_users[intl_charge_col],
                             title="Total Intl Charges vs Churn (Only Intl Plan Users)",
                             labels={churn_col:"Churn (original)", intl_charge_col:"Total Intl Charge"})
                st.plotly_chart(fig, use_container_width=True)
                st.markdown("**Insight:** Among international-plan users, churners show slightly higher total international charges than non-churners.")
                st.markdown("**Recommendation:** Consider discounted intl bundles or loyalty offers for heavy international users.")

elif chart_choice == "Churn by Tenure Bucket & Intl Plan":
    if "Tenure_Bucket" not in df.columns:
        st.warning("Tenure_Bucket not computed. Ensure 'Account_length' exists.")
    else:
        intl_col = next((c for c in df.columns if c.lower() == "international_plan"), None)
        if intl_col is None:
            st.warning("No 'International_plan' column found.")
        else:
            tenure_plan_churn = df.groupby(["Tenure_Bucket", intl_col])["_churn_num"].mean().reset_index()
            fig = px.bar(tenure_plan_churn, x="Tenure_Bucket", y="_churn_num", color=intl_col, barmode="group",
                         title="Churn Rate by Account Length Bucket and International Plan", labels={"_churn_num":"Churn Rate", "Tenure_Bucket":"Account Length Bucket"})
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("**Insights:** Across tenure buckets, customers with an International Plan have much higher churn rates. This group is small but high-risk.")
            st.markdown("**Recommendation:** Prioritize retention for international-plan customers with targeted pricing and support.")

elif chart_choice == "Churn by Tenure Bucket & Voice Mail Plan":
    if "Tenure_Bucket" not in df.columns:
        st.warning("Tenure_Bucket not computed. Ensure 'Account_length' exists.")
    else:
        vm_col = next((c for c in df.columns if c.lower() == "voice_mail_plan"), None)
        if vm_col is None:
            st.warning("No 'Voice_mail_plan' column found.")
        else:
            tenure_vm_churn = df.groupby(["Tenure_Bucket", vm_col])["_churn_num"].mean().reset_index()
            fig = px.bar(tenure_vm_churn, x="Tenure_Bucket", y="_churn_num", color=vm_col, barmode="group",
                         title="Churn Rate by Account Length Bucket and Voice Mail Plan", labels={"_churn_num":"Churn Rate", "Tenure_Bucket":"Account Length Bucket"})
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("**Insights:** Across all tenure buckets, customers with a Voice Mail Plan have much lower churn compared to those without.")
            st.markdown("**Recommendation:** Promote voicemail plans as a retention strategy.")

# End of page
st.markdown("---")
st.markdown("**Notes:** Hover on bars/lines to see exact values. Use the top-N slider to control how many states are shown.")
