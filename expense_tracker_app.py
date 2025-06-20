import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

FILE_NAME = "expense_tracker.csv"

def initialize_file():
    if not os.path.exists(FILE_NAME):
        df = pd.DataFrame(columns=["Date", "Category", "Amount", "Description"])
        df.to_csv(FILE_NAME, index=False)

def add_expense(date, category, amount, description):
    new_expense = pd.DataFrame({
        "Date": [date],
        "Category": [category],
        "Amount": [amount],
        "Description": [description]
    })

    df = pd.read_csv(FILE_NAME)
    df = pd.concat([df, new_expense], ignore_index=True)
    df.to_csv(FILE_NAME, index=False)

def view_expenses():
    df = pd.read_csv(FILE_NAME)
    return df

def view_by_category(category):
    df = pd.read_csv(FILE_NAME)
    return df[df["Category"].str.lower() == category.lower()]

def expense_summary():
    df = pd.read_csv(FILE_NAME)
    return df.groupby("Category")["Amount"].sum()

def clear_all_expenses():
    df = pd.DataFrame(columns=["Date", "Category", "Amount", "Description"])
    df.to_csv(FILE_NAME, index=False)

# ---------- Streamlit UI ----------
st.set_page_config(page_title="Personal Expense Tracker", layout="centered")
st.title("💰 Personal Expense Tracker")

initialize_file()

# Sidebar menu
menu = st.sidebar.selectbox("Menu", ["Add Expense", "View All Expenses", "Filter by Category", "Expense Summary"])

# Optional: Clear expenses section in sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("🧹 **Danger Zone**")
if st.sidebar.button("⚠️ Clear All Expenses"):
    confirm = st.sidebar.checkbox("Yes, I'm sure")
    if confirm:
        clear_all_expenses()
        st.sidebar.success("All expenses cleared successfully!")

# Main features
if menu == "Add Expense":
    st.subheader("➕ Add New Expense")
    date = st.date_input("Date")
    category = st.text_input("Category")
    amount = st.number_input("Amount", min_value=0.0, format="%.2f")
    description = st.text_input("Description")
    if st.button("Add"):
        if category and amount:
            add_expense(str(date), category, amount, description)
            st.success("Expense added successfully!")

elif menu == "View All Expenses":
    st.subheader("📋 All Expenses")
    df = view_expenses()
    if df.empty:
        st.warning("No expenses recorded yet.")
    else:
        st.dataframe(df)

elif menu == "Filter by Category":
    st.subheader("🔍 Filter by Category")
    cat = st.text_input("Enter Category")
    if st.button("Filter"):
        result = view_by_category(cat)
        if result.empty:
            st.info("No records found.")
        else:
            st.dataframe(result)

elif menu == "Expense Summary":
    st.subheader("📊 Expense Summary")

    df = pd.read_csv(FILE_NAME)
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
    df = df.dropna(subset=["Amount"])
    df["Category"] = df["Category"].str.strip().str.capitalize()
    summary = df.groupby("Category")["Amount"].sum()

    if summary.empty:
        st.warning("No data to summarize.")
    else:
        fig, ax = plt.subplots()
        ax.bar(summary.index, summary.values, color='skyblue')
        ax.set_title("Expenses by Category", fontsize=14)
        ax.set_ylabel("Total Amount")
        ax.set_xlabel("Category")
        plt.xticks(rotation=45)
        st.pyplot(fig)
