import pandas as pd
import sqlite3
import streamlit as st

# Database connection function
def create_connection():
    """ Create a connection to the SQLite database. """
    conn = sqlite3.connect('methods2.db')
    return conn

# Query the database
def query_database(selected_columns=None, search_query=None):
    """ Query the database for all data or specific columns with search capability. """
    conn = create_connection()
    cursor = conn.cursor()

    # Start building the query
    query = f'SELECT * FROM Methods'
    params = []

    # Add search condition if search_query is provided
    if search_query:
        search_conditions = []
        for col in selected_columns:
            if col != 'All Columns':  # Skip the 'All Columns' option
                search_conditions.append(f'"{col}" LIKE ?')  # Use parameterized queries to prevent SQL injection
                params.append(f'%{search_query}%')  # Wildcard search
        
        # Combine conditions with OR
        if search_conditions:
            query += ' WHERE ' + ' OR '.join(search_conditions)

    cursor.execute(query, params)

    # Fetch all results
    rows = cursor.fetchall()

    # Get the column names
    columns = [description[0] for description in cursor.description]

    # Convert the results to a DataFrame for better display
    df = pd.DataFrame(rows, columns=columns)

    # Filter based on selected columns
    if selected_columns and 'All Columns' not in selected_columns:
        df = df[selected_columns]

    # Close the connection
    conn.close()

    return df

# Streamlit App Interface
def main():
    st.title("Methods Database Query App")

    # Fetch column names from the database to allow users to choose
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(Methods)")
    columns_info = cursor.fetchall()
    conn.close()

    # Extract column names
    column_names = [col[1] for col in columns_info]
    column_names.insert(0, 'All Columns')  # Add 'All Columns' option

    # Sidebar - Selection
    st.sidebar.header("Search Parameters")
    selected_columns = st.sidebar.multiselect('Select columns to display:', column_names, default='All Columns')
    search_query = st.sidebar.text_input('Enter search query:')

    # Display the query results
    if st.sidebar.button("Search"):
        if selected_columns and search_query:
            df = query_database(selected_columns, search_query)
            if not df.empty:
                st.dataframe(df)
            else:
                st.write("No matching records found.")
        else:
            st.write("Please select columns and enter a search query.")

if __name__ == "__main__":
    main()
