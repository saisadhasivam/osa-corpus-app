import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

st.title("OSA Corpus Growth Model")
st.write("Compare Lifetime Fee vs Renewable Fee Membership Models")

# ------------------------------
# Sidebar Inputs
# ------------------------------
st.sidebar.header("Input Parameters")

# Alumni pool
alumni_pool = st.sidebar.number_input("Total Alumni (last 30 years)", min_value=1000, value=5400, step=100)
fresh_passouts = st.sidebar.number_input("New Graduates per Year", min_value=50, value=180, step=10)

# Fees
fee_500 = st.sidebar.number_input("Fresh Passouts Fee (₹)", min_value=100, value=500, step=100)
fee_2500 = st.sidebar.number_input("Lifetime Fee (₹)", min_value=500, value=2500, step=100)
fee_1000 = st.sidebar.number_input("Renewable Fee (₹)", min_value=500, value=1000, step=100)

# Dynamic renewal cycle
renewal_cycle = st.sidebar.number_input("Renewal Cycle (Years)", min_value=5, max_value=20, value=10, step=1)

# Scenario Toggle
scenario = st.sidebar.radio("Select Scenario", ["Conservative", "Moderate", "Optimistic"])

if scenario == "Conservative":
    signup_fresh = 50
    signup_old_2500 = 15
    signup_old_1000 = 25
elif scenario == "Moderate":
    signup_fresh = 70
    signup_old_2500 = 20
    signup_old_1000 = 35
else:  # Optimistic
    signup_fresh = 85
    signup_old_2500 = 30
    signup_old_1000 = 50

st.sidebar.write(f"Signup Fresh: {signup_fresh}% | Old Alumni at {fee_2500}: {signup_old_2500}% | Old Alumni at {fee_1000}: {signup_old_1000}%")

# Costs
portal_cost = st.sidebar.number_input("Portal Cost (₹ per year)", value=100000, step=10000)
audit_cost = st.sidebar.number_input("Audit Cost (₹ per year)", value=50000, step=10000)
gbm_cost = st.sidebar.number_input("GBM Cost per Year (₹)", value=100000, step=10000)
annual_cost = portal_cost + audit_cost + gbm_cost

# Financial assumptions
interest_rate = st.sidebar.slider("Corpus Interest Rate (%)", 1, 10, 5) / 100
donations = st.sidebar.number_input("Annual Donations (₹)", value=100000, step=10000)

years = st.sidebar.slider("Projection Horizon (Years)", 5, 30, 20)

# ------------------------------
# Simulation Function
# ------------------------------
def simulate(fee, old_signup_pct, renewal_cycle=None):
    members_old = int(alumni_pool * old_signup_pct / 100)
    corpus = members_old * fee
    corpus_over_time = [corpus]
    members_total = members_old
    
    for year in range(1, years + 1):
        # New fresh passouts
        new_fresh = int(fresh_passouts * signup_fresh / 100)
        
        # Fees collected this year
        yearly_fee = new_fresh * fee_500  # fresh joiners pay ₹500
        if renewal_cycle and year % renewal_cycle == 0:
            yearly_fee += members_total * fee  # renewal from all old members
        elif year == 1:
            yearly_fee += members_old * fee  # initial old alumni batch

        # Update members + corpus
        members_total += new_fresh
        corpus = corpus * (1 + interest_rate) + yearly_fee + donations - annual_cost
        corpus_over_time.append(corpus)
    
    return corpus_over_time

# ------------------------------
# Run Simulations
# ------------------------------
corpus_lifetime = simulate(fee=fee_2500, old_signup_pct=signup_old_2500, renewal_cycle=None)
corpus_renewable = simulate(fee=fee_1000, old_signup_pct=signup_old_1000, renewal_cycle=renewal_cycle)

# ------------------------------
# DataFrame for Display
# ------------------------------
df = pd.DataFrame({
    "Year": list(range(0, years + 1)),
    f"Corpus ₹{fee_2500} Lifetime": corpus_lifetime,
    f"Corpus ₹{fee_1000} (Every {renewal_cycle} Years)": corpus_renewable
})

st.subheader("Corpus Growth Over Time")
st.dataframe(df)

# ------------------------------
# Plot
# ------------------------------
plt.figure(figsize=(10, 6))
plt.plot(df["Year"], df[f"Corpus ₹{fee_2500} Lifetime"], 
         label=f"₹{fee_2500} Lifetime", marker="o")
plt.plot(df["Year"], df[f"Corpus ₹{fee_1000} (Every {renewal_cycle} Years)"], 
         label=f"₹{fee_1000} (Every {renewal_cycle} Years)", marker="s")

plt.xlabel("Year")
plt.ylabel("Corpus (₹ in Lakhs)")
plt.title("OSA Corpus Growth Projection")

# Convert y-axis to Lakhs
plt.gca().yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"{x/1e5:.0f} L"))

plt.legend()
st.pyplot(plt)

# ------------------------------
# Insights
# ------------------------------
st.subheader("Insights")
if max(df[f"Corpus ₹{fee_2500} Lifetime"]) > max(df[f"Corpus ₹{fee_1000} (Every {renewal_cycle} Years)"]):
    st.write(f"👉 ₹{fee_2500} Lifetime model builds corpus faster in the short term.")
else:
    st.write(f"👉 ₹{fee_1000} model with {renewal_cycle}-year renewal grows slower initially but overtakes long-term due to renewals and higher adoption.")

st.write("📌 More members = more engagement, which also means more donations and sponsorships beyond just fees.")
