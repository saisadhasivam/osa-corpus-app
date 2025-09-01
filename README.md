#  OSA Corpus Growth Simulator

This is a **Streamlit app** built to simulate and compare different membership fee models for our Old Students Association (OSA).  
It helps us understand how the **corpus fund** grows over time based on alumni participation, yearly expenses, and donations.

---

## Live Demo
   [Click here to open the app](https://osa-corpus-app-saisadhasivam.streamlit.app)

---

## Features

- Compare **Lifetime Fee model** vs **Renewable Fee model** side by side.
- Adjust all parameters dynamically from the sidebar:
  - **Total Alumni (last 30 years)**
  - **New Graduates per Year**
  - **Fresh Passouts Fee (₹)**
  - **Lifetime Fee (₹)**
  - **Renewable Fee (₹)**
  - **Renewal Cycle (Years)**
  - **Scenario (Conservative / Moderate / Optimistic)**
  - **Annual Costs (Portal, Audit, GBM)**
  - **Interest Rate (%)**
  - **Donations (₹)**
  - **Projection Horizon (Years)**

---

## How the Calculation Works

Each year, the model calculates:

1. **Fresh Joiners Fee**
   New Members × Fresh Fee

2. **Old Alumni Contribution**
- If Lifetime: One-time in year 1  
- If Renewable: At every renewal cycle
  Old Members × Lifetime/Renewal Fee

3. **Corpus Update**
   Corpus(t) = Corpus(t-1) × (1 + Interest Rate)
+ Fresh Fees + Renewal Fees + Donations
- Annual Costs

---

## 📈 Outputs

- **Table:** Year-by-year corpus values (in Lakhs)  
- **Graph:** Growth curves comparing Lifetime vs Renewable models  
- **Insights Section:** Explains which model performs better in short-term vs long-term  

---

## ⚡ Tech Stack

- [Streamlit](https://streamlit.io/) – for interactive web app  
- [Pandas](https://pandas.pydata.org/) – for data calculations  
- [Matplotlib](https://matplotlib.org/) – for plotting graphs  

---

## 👨‍💻 Author

Built by **Sai Sadhasivam** as part of the OSA initiative.
