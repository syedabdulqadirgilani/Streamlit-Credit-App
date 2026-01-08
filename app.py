# ==============================
# Shareholder & Manager Streamlit App
# ==============================

import streamlit as st

# ------------------------------
# Initialize in-memory storage
# ------------------------------
if "companies" not in st.session_state:
    st.session_state.companies = {}

if "shareholders" not in st.session_state:
    st.session_state.shareholders = {}

if "app_account" not in st.session_state:
    st.session_state.app_account = 0

if "current_user" not in st.session_state:
    st.session_state.current_user = None  # Track logged-in investor

# ------------------------------
# Sidebar for navigation
# ------------------------------
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", [
    "Home",
    "Register Company",
    "Investor Register/Login",
    "Buy Shares",
    "Sell Shares",
    "Registered Companies",
    "Monthly Contribution",
    "Annual Redistribution"
])

# ------------------------------
# Home Page
# ------------------------------
if page == "Home":
    st.title("Welcome to Shareholder & Manager App")
    st.write("""
    This app allows investors to register, buy/sell shares, 
    and track investments. Managers can register companies 
    and manage contributions.
    """)

# ------------------------------
# Investor Register/Login
# ------------------------------
elif page == "Investor Register/Login":
    st.title("Investor Portal")

    auth_option = st.radio("Choose an option:", ["Register", "Login"])

    if auth_option == "Register":
        st.subheader("Register as Investor")
        with st.form("register_form"):
            name = st.text_input("Name")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Register")
            if submitted:
                if not name or not password:
                    st.warning("Please enter both name and password.")
                elif name in st.session_state.shareholders:
                    st.warning(f"Investor '{name}' is already registered!")
                else:
                    st.session_state.shareholders[name] = {"password": password, "shares": {}}
                    st.success(f"Investor '{name}' registered successfully!")

    elif auth_option == "Login":
        st.subheader("Login")
        with st.form("login_form"):
            name = st.text_input("Name")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")
            if submitted:
                if name in st.session_state.shareholders:
                    if st.session_state.shareholders[name]["password"] == password:
                        st.session_state.current_user = name
                        st.success(f"Welcome, {name}!")
                    else:
                        st.error("Incorrect password!")
                else:
                    st.error("Investor not found. Please register first.")

# ------------------------------
# Register Company
# ------------------------------
elif page == "Register Company":
    st.title("Manager Portal: Register Company")
    with st.form("company_form"):
        company_name = st.text_input("Company Name")
        share_price = st.number_input("Share Price", min_value=0.01)
        monthly_earnings = st.number_input("Monthly Earnings", min_value=0.0)
        submitted = st.form_submit_button("Register Company")
        if submitted:
            if company_name in st.session_state.companies:
                st.warning(f"Company '{company_name}' already exists!")
            else:
                st.session_state.companies[company_name] = {
                    "price": share_price,
                    "monthly_earnings": monthly_earnings,
                    "contribution": 0.0
                }
                st.success(f"Company '{company_name}' registered successfully!")

# ------------------------------
# Buy Shares
# ------------------------------
elif page == "Buy Shares":
    if not st.session_state.current_user:
        st.warning("Please log in first to buy shares!")
    else:
        st.title("Buy Shares")
        if not st.session_state.companies:
            st.info("No companies available to buy shares.")
        else:
            company_list = list(st.session_state.companies.keys())
            company = st.selectbox("Select Company", company_list)
            shares_to_buy = st.number_input("Number of Shares", min_value=1)
            if st.button("Buy"):
                total_price = shares_to_buy * st.session_state.companies[company]["price"]
                st.session_state.app_account += 0.02 * total_price  # 2% to app account
                st.session_state.companies[company]["monthly_earnings"] += 0.98 * total_price
                user_shares = st.session_state.shareholders[st.session_state.current_user]["shares"]
                user_shares[company] = user_shares.get(company, 0) + shares_to_buy
                st.success(f"Bought {shares_to_buy} shares of '{company}' for ${total_price:.2f}.")

# ------------------------------
# Sell Shares
# ------------------------------
elif page == "Sell Shares":
    if not st.session_state.current_user:
        st.warning("Please log in first to sell shares!")
    else:
        st.title("Sell Shares")
        user_shares = st.session_state.shareholders[st.session_state.current_user]["shares"]
        if not user_shares:
            st.info("You don't own any shares to sell.")
        else:
            company = st.selectbox("Select Company to Sell", list(user_shares.keys()))
            max_shares = user_shares[company]
            shares_to_sell = st.number_input("Number of Shares", min_value=1, max_value=max_shares)
            if st.button("Sell"):
                total_price = shares_to_sell * st.session_state.companies[company]["price"]
                st.session_state.app_account += 0.02 * total_price
                st.session_state.companies[company]["monthly_earnings"] -= 0.98 * total_price
                user_shares[company] -= shares_to_sell
                if user_shares[company] == 0:
                    del user_shares[company]
                st.success(f"Sold {shares_to_sell} shares of '{company}' for ${total_price:.2f}.")

# ------------------------------
# Display Registered Companies
# ------------------------------
elif page == "Registered Companies":
    st.title("Registered Companies")
    if st.session_state.companies:
        for name, data in st.session_state.companies.items():
            st.write(f"**{name}**")
            st.write(f"- Share Price: ${data['price']}")
            st.write(f"- Monthly Earnings: ${data['monthly_earnings']:.2f}")
            st.write(f"- Contribution: ${data['contribution']:.2f}")
            st.write("---")
    else:
        st.info("No companies registered yet.")

# ------------------------------
# Monthly Contribution
# ------------------------------
elif page == "Monthly Contribution":
    st.title("Monthly Contribution")
    for company, data in st.session_state.companies.items():
        contribution = 0.02 * data["monthly_earnings"]
        st.session_state.companies[company]["contribution"] += contribution
        st.session_state.app_account += contribution
        st.success(f"{company} contributed ${contribution:.2f} this month.")

# ------------------------------
# Annual Redistribution
# ------------------------------
elif page == "Annual Redistribution":
    st.title("Annual Redistribution")
    total_contributions = sum([data["contribution"] for data in st.session_state.companies.values()])
    if total_contributions == 0:
        st.info("No contributions to redistribute.")
    else:
        for company, data in st.session_state.companies.items():
            share_ratio = data["contribution"] / total_contributions
            redistribution_amount = 0.7 * st.session_state.app_account * share_ratio
            st.session_state.companies[company]["monthly_earnings"] += redistribution_amount
            st.success(f"{company} received ${redistribution_amount:.2f} from redistribution.")
        st.session_state.app_account = 0
        st.success("Annual redistribution complete. App account reset to $0.")
