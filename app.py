# ==============================
# Shareholder & Manager Streamlit App
# ==============================

import streamlit as st

# ------------------------------
# In-memory data storage
# ------------------------------
if "companies" not in st.session_state:
    st.session_state.companies = {}

if "shareholders" not in st.session_state:
    st.session_state.shareholders = {}

if "app_account" not in st.session_state:
    st.session_state.app_account = 0

# Add these pages to your existing Streamlit app
# ==============================

# ------------------------------
# Sidebar for navigation (update)
# ------------------------------
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", [
    "Home",
    "Register Company",
    "Register Investor",       # New page
    "Buy Shares",
    "Sell Shares",
    "Registered Companies",    # New page
    "Monthly Contribution",
    "Annual Redistribution"
])

# ------------------------------
# Register Investor (Shareholder)
# ------------------------------
if page == "Register Investor":
    st.title("Register Investor")
    with st.form("investor_form"):
        investor_name = st.text_input("Investor Name")
        submitted = st.form_submit_button("Register")
        if submitted:
            if investor_name in st.session_state.shareholders:
                st.warning(f"Investor '{investor_name}' is already registered!")
            else:
                st.session_state.shareholders[investor_name] = {}
                st.success(f"Investor '{investor_name}' registered successfully!")

# ------------------------------
# Display Registered Companies
# ------------------------------
elif page == "Registered Companies":
    st.title("Registered Companies")
    if st.session_state.companies:
        for name, data in st.session_state.companies.items():
            st.write(f"**{name}**")
            st.write(f"- Share Price: {data['price']}")
            st.write(f"- Monthly Earnings: {data['monthly_earnings']:.2f}")
            st.write(f"- Contribution: {data['contribution']:.2f}")
            st.write("---")
    else:
        st.info("No companies registered yet.")
