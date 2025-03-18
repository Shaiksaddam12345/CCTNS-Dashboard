

import streamlit as st
import pandas as pd
import urllib.parse
import os
import openpyxl

# Set Page Configuration
st.set_page_config(page_title="User Login", page_icon="🔑", layout="centered")

# File Path to User Data
file_path = r"C:\\Users\\YS244WK\\OneDrive - EY\\Desktop\\python\\user_data.xlsx"

# Function to Load User Data
@st.cache_data
def load_user_data(file_path):
    try:
        if not os.path.exists(file_path):
            st.error("User data file not found. Please check the file path.")
            return {}
        
        df = pd.read_excel(file_path, dtype=str, engine="openpyxl")
        
        return {
            row["Username"]: {
                "Password": row["Password"],
                "Power BI Username": row["Power BI Username"],
                "Dashboard URL": row["Dashboard URL"]
            }
            for _, row in df.iterrows()
        }
    except PermissionError:
        st.error("Permission denied: Close the Excel file and try again.")
        return {}
    except Exception as e:
        st.error(f"Error loading user data: {e}")
        return {}

# Load User Data
user_data = load_user_data(file_path)

TABLE_NAME = "selfassessment"  # Update with actual table name
COLUMN_NAME = "fk_company_id"  # Update with actual column name

st.title("🔐 User Login")

# Username & Password Input
username = st.text_input("Username")
password = st.text_input("Password", type="password")

# Login Button
if st.button("Login"):
    if username in user_data and user_data[username]["Password"] == password:
        st.success(f"Welcome, {username}!")

        power_bi_username = user_data[username]["Power BI Username"]
        dashboard_url = user_data[username]["Dashboard URL"]

        # Encode filter for Power BI URL
        encoded_filter = urllib.parse.quote(f"{TABLE_NAME}/{COLUMN_NAME} eq '{power_bi_username}'")

        # Generate Power BI URL with user filter
        power_bi_url = f"{dashboard_url}&filter={encoded_filter}"

        # Display Power BI link
        st.markdown(f"[Open Power BI Report]({power_bi_url})", unsafe_allow_html=True)
    else:
        st.error("Invalid username or password")