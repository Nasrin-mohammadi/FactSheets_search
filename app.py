import pandas as pd
import sqlite3
import streamlit as st
from main import query_database

# Streamlit app
st.title('FactSheets')

# Create a connection for Streamlit
try:
    conn = sqlite3.connect('methods2.db')
except Exception as e:
    st.error(f"Error connecting to the database: {e}")

# Check if the database has the Methods table
table_exists_query = """
    SELECT name FROM sqlite_master WHERE type='table' AND name='Methods';
"""
table_exists = pd.read_sql(table_exists_query, conn)

if not table_exists.empty:
    # Fetch all columns from the Methods table
    query = 'SELECT * FROM Methods LIMIT 1;'  # Fetch a single row to get column names
    try:
        data = pd.read_sql(query, conn)
        all_columns = data.columns.tolist()  # Get list of all column names
    except Exception as e:
        st.error(f"Error fetching columns: {e}")

    # Multiselect for users to choose columns to display, including "All Columns"
    selected_columns = st.multiselect(
        'Select columns to display (select "All Columns" to display all):',
        options=['All Columns'] + all_columns,
        default=[]
    )

    # Input for search query
    search_query = st.text_input("Search in selected columns:")

    # Determine the actual columns to select based on user input
    if "All Columns" in selected_columns:
        selected_columns = all_columns  # Select all columns if "All Columns" is chosen
    else:
        selected_columns = [col for col in selected_columns if col != "All Columns"]

    # Fetch and display the selected columns
    if selected_columns:
        data = query_database('Methods', selected_columns, search_query)
        if not data.empty:
            st.write(data)
        else:
            st.write("No results found for the given search query.")
else:
    st.error("Methods table does not exist in the database.")

# Close the Streamlit database connection
conn.close()
