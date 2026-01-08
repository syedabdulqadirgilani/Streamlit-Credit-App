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

# ------------------------------
# Sidebar for navigation
# ------------------------------
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Register Company", "Buy Shares", "Sell Shares", "Monthly Contribution", "Annual Redistribution"])

# ------------------------------
# Home page
# ------------------------------
if page == "Home":
    st.title("Shareholder & Manager App")
    st.write("Welcome! Use the sidebar to navigate the app.")
    st.write(f"App account balance: {st.session_state.app_account:.2f}")
    st.write("### Companies:")
    if st.session_state.companies:
        for name, data in st.session_state.companies.items():
            st.write(f"- **{name}** | Price: {data['price']} | Monthly Earnings: {data['monthly_earnings']:.2f} | Contribution: {data['contribution']:.2f}")
    else:
        st.write("No companies registered yet.")

    st.write("### Shareholders:")
    if st.session_state.shareholders:
        for user, holdings in st.session_state.shareholders.items():
            st.write(f"- **{user}**: {holdings}")
    else:
        st.write("No shareholders yet.")

# ------------------------------
# Register company
# ------------------------------
elif page == "Register Company":
    st.title("Register Company")
    with st.form("register_form"):
        name = st.text_input("Company Name")
        price = st.number_input("Share Price", min_value=0.01, step=0.01)
        submitted = st.form_submit_button("Register")
        if submitted:
            st.session_state.companies[name] = {"price": price, "monthly_earnings": 0, "contribution": 0}
            st.success(f"Company '{name}' registered!")

# ------------------------------
# Buy shares
# ------------------------------
elif page == "Buy Shares":
    st.title("Buy Shares")
    with st.form("buy_form"):
        user = st.text_input("Shareholder Name")
        company = st.selectbox("Company", list(st.session_state.companies.keys()))
        shares = st.number_input("Number of Shares", min_value=1, step=1)
        submitted = st.form_submit_button("Buy")
        if submitted:
            total = st.session_state.companies[company]["price"] * shares
            fee = total * 0.02
            st.session_state.app_account += fee
            st.session_state.companies[company]["monthly_earnings"] += (total - fee)

            if user not in st.session_state.shareholders:
                st.session_state.shareholders[user] = {}
            st.session_state.shareholders[user][company] = st.session_state.shareholders[user].get(company, 0) + shares

            st.success(f"{user} bought {shares} shares of {company}!")

# ------------------------------
# Sell shares
# ------------------------------
elif page == "Sell Shares":
    st.title("Sell Shares")
    with st.form("sell_form"):
        seller = st.selectbox("Seller Name", list(st.session_state.shareholders.keys()))
        buyer = st.text_input("Buyer Name")
        company = st.selectbox("Company", list(st.session_state.companies.keys()))
        shares = st.number_input("Shares to Sell", min_value=1, step=1)
        submitted = st.form_submit_button("Sell")
        if submitted:
            if st.session_state.shareholders[seller].get(company, 0) < shares:
                st.error("Not enough shares to sell")
            else:
                total = st.session_state.companies[company]["price"] * shares
                fee = total * 0.02
                st.session_state.app_account += fee

                st.session_state.shareholders[seller][company] -= shares

                if buyer not in st.session_state.shareholders:
                    st.session_state.shareholders[buyer] = {}
                st.session_state.shareholders[buyer][company] = st.session_state.shareholders[buyer].get(company, 0) + shares

                st.success(f"{seller} sold {shares} shares of {company} to {buyer}!")

# ------------------------------
# Monthly contribution
# ------------------------------
elif page == "Monthly Contribution":
    st.title("Monthly Contribution")
    for company in st.session_state.companies:
        contribution = st.session_state.companies[company]["monthly_earnings"] * 0.02
        st.session_state.companies[company]["contribution"] += contribution
        st.session_state.app_account += contribution
        st.session_state.companies[company]["monthly_earnings"] = 0
    st.success("Monthly contributions processed!")

# ------------------------------
# Annual redistribution
# ------------------------------
elif page == "Annual Redistribution":
    st.title("Annual Redistribution")
    total = sum(st.session_state.companies[c]["contribution"] for c in st.session_state.companies)

    if total == 0:
        st.warning("No contributions yet")
    else:
        distributable = total * 0.70
        for company in st.session_state.companies:
            ratio = st.session_state.companies[company]["contribution"] / total
            payout = distributable * ratio
            st.write(f"**{company}** received {payout:.2f}")
