import streamlit as st
import pandas as pd
import plotly.express as px

# ================== PAGE SETUP ==================
st.set_page_config(page_title="Analysis & Insights", layout="wide")
st.title("📊 Telecom Churn Analysis & Insights")

# ================== LOAD DATA ==================
@st.cache_data
def load_data(train_path="/Users/mohammedmahmood/Desktop/Telecom_Churn_App/pages/data/churn-bigml-80.csv", test_path="/Users/mohammedmahmood/Desktop/Telecom_Churn_App/pages/data/churn-bigml-20.csv"):
    train_df = pd.read_csv(train_path)
    test_df = pd.read_csv(test_path)
    df = pd.concat([train_df, test_df], ignore_index=True)
    df.columns = [c.strip().replace(" ", "_") for c in df.columns]
    if df["Churn"].dtype == object:
        df["_churn_num"] = df["Churn"].apply(lambda x: 1 if str(x).lower() in ("yes", "y", "true", "1") else 0)
    else:
        df["_churn_num"] = df["Churn"]
    return df

df = load_data()

# ================== SIDEBAR ==================
st.sidebar.header("📂 Select Analysis Category")
category = st.sidebar.selectbox(
    "Choose Analysis Section:",
    ["1️⃣ Customer Profile", "2️⃣ Service Plans", "3️⃣ Customer Service", "4️⃣ Usage & Charges", "5️⃣ Multivariate Analysis"]
)

# Sub-analysis for each category
if category == "1️⃣ Customer Profile":
    sub = st.sidebar.selectbox(
        "Select analysis:",
        ["1 - Churn Rate by State", "2 - Account Length vs Churn"]
    )

# ================== MAIN AREA ==================
st.markdown("---")

if category == "1️⃣ Customer Profile" and sub == "1 - Churn Rate by State":
    st.markdown("### 1️⃣ Does churn rate vary by State?")
    st.markdown("#### We want to know: Are there specific geographic regions with higher churn?")

    if "State" in df.columns and "_churn_num" in df.columns:
        state_churn = df.groupby("State")["_churn_num"].sum().reset_index().sort_values("_churn_num", ascending=False).head(20)

        fig = px.bar(
            state_churn,
            x="State",
            y="_churn_num",
            title="Top 20 States by Churn Count",
            labels={"_churn_num": "Churn Count"}
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("**Insight:** States like WV, MN, and NY have the highest number of churners (over 80–100 each), while states like NJ and NC are lower (~68).")
        st.markdown("**Recommendation:** Investigate high-churn states for possible regional causes such as coverage issues, pricing, or customer service gaps.")
        st.download_button("📥 Download Data (CSV)", data=state_churn.to_csv(index=False).encode("utf-8"), file_name="state_churn.csv")
    else:
        st.warning("Columns 'State' or 'Churn' not found in the dataset.")

elif category == "1️⃣ Customer Profile" and sub == "2 - Account Length vs Churn":
    st.markdown("### 2️⃣ Account Length vs Churn")
    st.markdown("#### We want to see if tenure (time with company) affects churn rate.")

    if "Account_length" in df.columns and "_churn_num" in df.columns:
        fig = px.box(
            df,
            x="Churn",
            y="Account_length",
            title="Account Length vs Churn",
            labels={"Churn": "Churn (0=No, 1=Yes)", "Account_length": "Account Length (days)"}
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("**Insight:** Account length looks very similar for churners and non-churners. The median and spread overlap a lot, meaning tenure alone does not explain churn.")
        st.markdown("**Recommendation:** Customer loyalty is not guaranteed by tenure — focus on service quality and engagement to reduce churn.")
    else:
        st.warning("Columns 'Account_length' or 'Churn' not found in the dataset.")


# ================== 2. Service Plans ==================
elif category == "2️⃣ Service Plans":
    sub = st.sidebar.selectbox(
        "Select analysis:",
        ["3 - Churn by International Plan", "4 - Churn by Voice Mail Plan"]
    )

    # ---------- 3. Churn by International Plan ----------
    if sub == "3 - Churn by International Plan":
        st.markdown("### 3️⃣ Do customers with an International Plan churn more often?")
        st.markdown("#### High-value but also sensitive segment")

        if "International_plan" in df.columns and "_churn_num" in df.columns:
            intl_churn = df.groupby("International_plan")["_churn_num"].mean().reset_index()
            fig = px.bar(
                intl_churn,
                x="International_plan",
                y="_churn_num",
                title="Churn Rate by International Plan",
                labels={"_churn_num": "Churn Rate"}
            )
            fig.update_yaxes(tickformat=".0%")
            st.plotly_chart(fig, use_container_width=True)

            st.markdown("**Insight:** Customers with an International Plan churn much more (~42%) compared to those without (~11%). This shows that international users are far more likely to leave.")
            st.markdown("**Recommendation:** Since international users are high-value but high-risk, the company should focus on competitive pricing, better support, or loyalty perks to reduce churn in this premium segment.")

            st.download_button("📥 Download Data (CSV)", data=intl_churn.to_csv(index=False).encode("utf-8"), file_name="intl_plan_churn.csv")
        else:
            st.warning("Columns 'International_plan' or 'Churn' not found in the dataset.")

    # ---------- 4. Churn by Voice Mail Plan ----------
    elif sub == "4 - Churn by Voice Mail Plan":
        st.markdown("### 4️⃣ Is there a difference in churn between customers with and without a Voice Mail Plan?")
        st.markdown("#### Want to know: Does having extra services reduce churn?")

        if "Voice_mail_plan" in df.columns and "_churn_num" in df.columns:
            vm_churn = df.groupby("Voice_mail_plan")["_churn_num"].mean().reset_index()
            fig = px.bar(
                vm_churn,
                x="Voice_mail_plan",
                y="_churn_num",
                title="Churn Rate by Voice Mail Plan",
                labels={"_churn_num": "Churn Rate"}
            )
            fig.update_yaxes(tickformat=".0%")
            st.plotly_chart(fig, use_container_width=True)

            st.markdown("**Insight:** Customers with a Voice Mail Plan churn less (~9%) compared to those without (~17%). Extra services seem to increase loyalty.")
            st.markdown("**Recommendation:** Promoting Voice Mail Plans could help reduce churn and improve overall customer retention.")

            st.download_button("📥 Download Data (CSV)", data=vm_churn.to_csv(index=False).encode("utf-8"), file_name="voice_mail_plan_churn.csv")
        else:
            st.warning("Columns 'Voice_mail_plan' or 'Churn' not found in the dataset.")


# ================== 3. Customer Service ==================
elif category == "3️⃣ Customer Service":
    sub = st.sidebar.selectbox(
        "Select analysis:",
        ["5 - Churn vs Number of Customer Service Calls", "6 - Churn by Service Calls Split by Intl Plan"]
    )

    # ---------- 5. Churn vs Customer Service Calls ----------
    if sub == "5 - Churn vs Number of Customer Service Calls":
        st.markdown("### 5️⃣ How does churn rate increase with Customer Service Calls?")
        st.markdown("#### We want to know: After how many calls does churn start to jump significantly?")

        if "Customer_service_calls" in df.columns and "_churn_num" in df.columns:
            service_churn = df.groupby("Customer_service_calls")["_churn_num"].mean().reset_index()

            fig = px.line(
                service_churn,
                x="Customer_service_calls",
                y="_churn_num",
                markers=True,
                title="Churn Rate vs Number of Customer Service Calls",
                labels={"_churn_num": "Churn Rate", "Customer_service_calls": "Customer Service Calls"}
            )
            fig.update_yaxes(tickformat=".0%")
            st.plotly_chart(fig, use_container_width=True)

            st.markdown("**Insight:** Churn rate stays low for 0–2 service calls but jumps sharply after 3+ calls, reaching above 40%, and hits nearly 100% for 9 calls. High service calls are a strong signal of dissatisfaction.")
            st.markdown("**Recommendation:** Customers who call support more than 3 times should be flagged as high-risk and prioritized for fast resolution, proactive outreach, or escalation to retention teams before they leave.")

            st.download_button("📥 Download Data (CSV)", data=service_churn.to_csv(index=False).encode("utf-8"), file_name="service_calls_churn.csv")
        else:
            st.warning("Columns 'Customer_service_calls' or 'Churn' not found in the dataset.")

    # ---------- 6. Churn by Service Calls Split by Intl Plan ----------
    elif sub == "6 - Churn by Service Calls Split by Intl Plan":
        st.markdown("### 6️⃣ Is the effect of Customer Service Calls stronger for International Plan users?")
        st.markdown("#### Exploring how churn behavior changes between customers with and without International Plans.")

        if "Customer_service_calls" in df.columns and "International_plan" in df.columns and "_churn_num" in df.columns:
            interaction = df.groupby(["International_plan", "Customer_service_calls"])["_churn_num"].mean().reset_index()

            fig = px.line(
                interaction,
                x="Customer_service_calls",
                y="_churn_num",
                color="International_plan",
                markers=True,
                title="Churn by Service Calls (Split by International Plan)",
                labels={"_churn_num": "Churn Rate", "Customer_service_calls": "Customer Service Calls"}
            )
            fig.update_yaxes(tickformat=".0%")
            st.plotly_chart(fig, use_container_width=True)

            st.markdown("**Insight:** For customers with an International Plan, churn is much higher from the start (~40–45%) and rises faster with more service calls, reaching 100% after 5+ calls.")
            st.markdown("**Recommendation:** Dissatisfied premium customers (Intl Plan + repeated service calls) are the most at risk. They should get priority handling and special retention offers to avoid losing this high-value segment.")

            st.download_button("📥 Download Data (CSV)", data=interaction.to_csv(index=False).encode("utf-8"), file_name="intl_plan_service_calls_churn.csv")
        else:
            st.warning("Columns 'Customer_service_calls' or 'International_plan' not found in the dataset.")

# ================== 4. Usage & Charges ==================
elif category == "4️⃣ Usage & Charges":
    sub = st.sidebar.selectbox(
        "Select analysis:",
        ["7 - Churn vs Total Intl Charges (Intl Users Only)"]
    )

    # ---------- 7. Churn vs Total Intl Charge ----------
    if sub == "7 - Churn vs Total Intl Charges (Intl Users Only)":
        st.markdown("### 7️⃣ For international users, is churn linked to higher Total International Charges?")
        st.markdown("#### We want to know: Are competitors offering better international pricing?")

        if "International_plan" in df.columns and "Total_intl_charge" in df.columns and "_churn_num" in df.columns:
            intl_users = df[df["International_plan"].astype(str).str.lower() == "yes"]

            fig = px.box(
                intl_users,
                x="Churn",
                y="Total_intl_charge",
                title="Total Intl Charges vs Churn (Only Intl Plan Users)",
                labels={"Churn": "Churn (0=No, 1=Yes)", "Total_intl_charge": "Total International Charges"}
            )
            st.plotly_chart(fig, use_container_width=True)

            st.markdown("**Insight:** Among international plan users, churners show slightly higher total international charges than non-churners. This suggests that heavy international spenders are more likely to leave.")
            st.markdown("**Recommendation:** Competitors offering cheaper international rates could be pulling away these high-spending customers. To reduce churn, the company should consider discounted international bundles or loyalty offers for heavy international users.")
            
            st.download_button("📥 Download Data (CSV)", data=intl_users.to_csv(index=False).encode("utf-8"), file_name="intl_users_charges.csv")
        else:
            st.warning("Columns 'International_plan' or 'Total_intl_charge' not found in the dataset.")

# ================== 5. Multivariate Analysis ==================
elif category == "5️⃣ Multivariate Analysis":
    sub = st.sidebar.selectbox(
        "Select analysis:",
        ["8 - Churn by Tenure Bucket & International Plan", "9 - Churn by Tenure Bucket & Voice Mail Plan"]
    )

    # ---------- 8. Churn by Tenure Bucket & International Plan ----------
    if sub == "8 - Churn by Tenure Bucket & International Plan":
        st.markdown("### 8️⃣ Churn by Account Length Bucket and International Plan")
        st.markdown("#### Does churn risk differ by tenure (New, Mid, Long) for customers with and without an International Plan?")

        if "Account_length" in df.columns and "International_plan" in df.columns and "_churn_num" in df.columns:
            df["Tenure_Bucket"] = pd.cut(
                df["Account_length"],
                bins=[1, 50, 150, df["Account_length"].max()],
                labels=["New", "Mid", "Long"]
            )

            tenure_plan_churn = df.groupby(["Tenure_Bucket", "International_plan"])["_churn_num"].mean().reset_index()

            fig = px.bar(
                tenure_plan_churn,
                x="Tenure_Bucket",
                y="_churn_num",
                color="International_plan",
                barmode="group",
                title="Churn Rate by Account Length Bucket and International Plan",
                labels={"_churn_num": "Churn Rate", "Tenure_Bucket": "Account Length Bucket"}
            )
            fig.update_yaxes(tickformat=".0%")
            st.plotly_chart(fig, use_container_width=True)

            st.markdown("**Insight:** Across all tenure buckets (New, Mid, Long), customers with an International Plan have much higher churn rates (~30–45%) compared to those without (~10–12%). The gap is consistent, showing that plan type is a strong churn indicator. Despite being fewer in number, international plan users contribute disproportionately to churn.")
            st.markdown("**Recommendation:** These high-value but high-risk customers should receive targeted offers, better international pricing, and enhanced support to reduce churn.")

            st.download_button("📥 Download Data (CSV)", data=tenure_plan_churn.to_csv(index=False).encode("utf-8"), file_name="tenure_bucket_intl_plan.csv")
        else:
            st.warning("Required columns not found: 'Account_length', 'International_plan', '_churn_num'.")

    # ---------- 9. Churn by Tenure Bucket & Voice Mail Plan ----------
    elif sub == "9 - Churn by Tenure Bucket & Voice Mail Plan":
        st.markdown("### 9️⃣ Churn by Account Length Bucket and Voice Mail Plan")
        st.markdown("#### Does churn risk differ by tenure for customers with and without a Voice Mail Plan?")

        if "Tenure_Bucket" not in df.columns and "Account_length" in df.columns:
            df["Tenure_Bucket"] = pd.cut(
                df["Account_length"],
                bins=[1, 50, 150, df["Account_length"].max()],
                labels=["New", "Mid", "Long"]
            )

        if "Voice_mail_plan" in df.columns and "_churn_num" in df.columns:
            tenure_vm_churn = df.groupby(["Tenure_Bucket", "Voice_mail_plan"])["_churn_num"].mean().reset_index()

            fig = px.bar(
                tenure_vm_churn,
                x="Tenure_Bucket",
                y="_churn_num",
                color="Voice_mail_plan",
                barmode="group",
                title="Churn Rate by Account Length Bucket and Voice Mail Plan",
                labels={"_churn_num": "Churn Rate", "Tenure_Bucket": "Account Length Bucket"}
            )
            fig.update_yaxes(tickformat=".0%")
            st.plotly_chart(fig, use_container_width=True)

            st.markdown("**Insight:** Across all tenure buckets, customers with a Voice Mail Plan have much lower churn (~5–9%) compared to those without (~15–17%). The churn gap is consistent, meaning voicemail helps retain customers regardless of tenure.")
            st.markdown("**Recommendation:** Promoting Voice Mail Plans can be an effective retention strategy. It benefits both new and long-term customers, improving engagement and satisfaction.")

            st.download_button("📥 Download Data (CSV)", data=tenure_vm_churn.to_csv(index=False).encode("utf-8"), file_name="tenure_bucket_voicemail.csv")
        else:
            st.warning("Required columns not found: 'Voice_mail_plan' or 'Churn'.")

# ================== FINAL INSIGHTS & RECOMMENDATIONS ==================

with st.expander(" ", expanded=False):  # نخلي العنوان فاضي لأننا هنضيفه يدويًا بخط أكبر
    st.markdown("""
        <div style='text-align:center; padding:10px 0;'>
            <h1 style='color:#1565C0; font-size:36px; font-weight:800; letter-spacing:1px;'>
                 Final Summary & Recommendations
            </h1>
            <hr style='border:2px solid #1565C0; width:60%; margin:auto;'>
        </div>
    """, unsafe_allow_html=True)


    st.markdown("""
    <div style='font-size:17px; line-height:1.8; text-align:justify;'>

    ###  <span style='color:#1976D2;'>Overall Insights Summary</span>

    • **Customer Profile:**  
      States like <b>WV, MN, and NY</b> have the highest churn, suggesting regional churn imbalance.  
      <b>Account length</b> alone doesn’t predict churn — even loyal customers leave.

    • **Service Plans:**  
      Customers with an <b>International Plan</b> churn almost <b>4× more</b> than others.  
      Those with a <b>Voice Mail Plan</b> churn less (~9% vs 17%), meaning add-on services increase loyalty.

    • **Customer Service:**  
      Churn jumps dramatically after <b>3+ customer service calls</b> — a clear dissatisfaction signal.  
      For <b>International Plan</b> users, churn reaches nearly <b>100%</b> after multiple calls.

    • **Usage & Charges:**  
      Among international users, <b>higher total international charges</b> correlate with churn — heavy spenders are leaving.

    • **Multivariate Findings:**  
      Across all tenure buckets, <b>International Plan</b> users churn more (~30–45%) than others (~10–12%).  
      <b>Voice Mail Plan</b> users consistently show lower churn across every tenure level.

    <br>
    <hr style='margin:10px 0;'>

    ###  <span style='color:#43A047;'>Strategic Recommendations</span>

    1.  <b>Focus retention efforts on high-churn regions</b> (WV, MN, NY).  
       Investigate local issues such as pricing, signal quality, and support response time.

    2.  <b>Revisit International Plan strategy.</b>  
       Provide better pricing, loyalty points, or premium support to reduce churn among high-value users.

    3.  <b>Promote add-on services like Voice Mail Plans.</b>  
       They strongly correlate with higher customer retention.

    4.  <b>Flag customers with more than 3 service calls as “high-risk.”</b>  
       Offer proactive help or escalate them to retention teams early.

    5.  <b>Offer discounts for heavy international callers.</b>  
       Competitors may be stealing these customers through cheaper rates.

    6.  <b>Use predictive analytics to prevent churn before it happens.</b>  
       Automatically detect high-risk users and trigger retention campaigns.

    <br>
    <hr style='margin:10px 0;'>

    ###  <span style='color:#E53935;'>Key Takeaway</span>
    <b>Churn is driven by experience, cost, and support — not tenure.</b>  
    Reducing churn requires <b>personalized care, proactive retention, and competitive offers</b>,  
    especially for <b>International Plan</b> customers and those making frequent support calls.

    </div>
    """, unsafe_allow_html=True)

    st.success("✅ This summary unifies insights and recommendations from all analyses for strategic decision-making.")
