import streamlit as st
import pandas as pd

# Initialize in-memory storage
if "expenses" not in st.session_state:
    st.session_state.expenses = pd.DataFrame(columns=["Date", "Category", "Amount", "Description"])

def add_expense(date, category, amount, description):
    new_row = {"Date": date, "Category": category, "Amount": amount, "Description": description}
    st.session_state.expenses = pd.concat([st.session_state.expenses, pd.DataFrame([new_row])], ignore_index=True)

def clear_all_expenses():
    st.session_state.expenses = pd.DataFrame(columns=["Date", "Category", "Amount", "Description"])

def view_by_category(category):
    return st.session_state.expenses[st.session_state.expenses["Category"].str.lower() == category.lower()]

# UI
st.set_page_config(page_title="Temporary Expense Tracker", layout="centered")
st.title("💰 Personal Expense Tracker")

menu = st.sidebar.selectbox("Menu", ["Add Expense", "View All Expenses", "Filter by Category"])

st.sidebar.markdown("---")
with st.sidebar.expander("⚠️ Clear All Expenses"):
    confirm_clear = st.checkbox("Yes, I want to clear all data")
    if st.button("Delete All Expenses"):
        if confirm_clear:
            clear_all_expenses()
            st.success("✅ All expenses cleared.")
        else:
            st.warning("☑️ Please confirm by checking the box.")

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
    if st.session_state.expenses.empty:
        st.warning("No expenses recorded yet.")
    else:
        st.dataframe(st.session_state.expenses)

elif menu == "Filter by Category":
    st.subheader("🔍 Filter by Category")
    cat = st.text_input("Enter Category")
    if st.button("Filter"):
        result = view_by_category(cat)
        if result.empty:
            st.info("No records found.")
        else:
            st.dataframe(result)
