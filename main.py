import pandas as pd
import sqlite3

# Load the Excel file
#file_path = '/Users/__nasrin__/Desktop/SQL db/240930_DECODE_Task1.5_List_Task&Methods_for_FS.xlsx'  # Update with the path to your workbook
#sheets = ['Methods T1.2', 'Methods T1.3', 'Methods T1.4', 'Methods T2.1', 'Methods T2.2', 'Methods T2.4']  # List your sheet names

# Create a connection to SQLite
conn = sqlite3.connect('methods2.db')
cursor = conn.cursor()

# Create the Methods table in SQL
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Methods (
        Partner TEXT,
        Contact_person_in_DECODE TEXT,
        Email_Adress_of_the_Contact_Person TEXT,
        Associated_to_DECODE_Task TEXT,
        Method_type TEXT,
        Name_of_the_method_or_technique TEXT,
        Objective_of_the_method_within_the_project TEXT,
        Method_maturity TEXT,
        Is_part_of_method TEXT,
        Unique_ID TEXT,
        Method_category TEXT,
        Scale TEXT,
        Documentation TEXT,
        Cost_and_time TEXT,
        Accessibility TEXT,
        Interoperability TEXT,
        Relevance_for_DECODE_use_cases TEXT,
        Applicability_beyond_DECODE TEXT,
        For_Models_Model_requirements TEXT,
        For_Models_Model_assumptions TEXT,
        For_Models_Implementation_details TEXT,
        For_Models_Parameterization_and_validation_incl_accuracy_and_sensitivity_to_inputs TEXT,
        For_Models_Range_of_validity TEXT,
        For_Experimental_Methods_Method_Requirements TEXT,
        For_Experimental_Methods_Method_Assumptions TEXT,
        For_Experimental_Methods_Implementation_details TEXT,
        For_Experimental_Methods_Preparation TEXT,
        For_Experimental_Methods_Validation TEXT,
        For_Experimental_Methods_Range_of_validity TEXT,
        For_Manufacturing_Methods_Process_steps TEXT,
        For_Manufacturing_Methods_Implementation_details TEXT,
        For_Manufacturing_Methods_Validation_and_accuracy_of_the_method TEXT,
        For_Manufacturing_Methods_Range_of_processability TEXT,
        Inputs TEXT,
        Scale_of_inputs TEXT,
        Details_comments_to_Inputs TEXT,
        Outputs TEXT,
        Scale_of_outputs TEXT,
        Details_comments_to_outputs TEXT
    )
''')

# Iterate through each sheet and insert data into the SQL table
for sheet in sheets:
    df = pd.read_excel(file_path, sheet_name=sheet)

    # Print the columns to verify their names
    print(f"Columns in sheet '{sheet}': {df.columns.tolist()}")

    # Select only the columns as they appear in the Excel sheets
    common_columns = [
        'Partner',
        'Contact_person_in_DECODE',
        'Email_Adress_of_the_Contact_Person',
        'Associated_to_DECODE_Task',
        'Method_type',
        'Name_of_the_method_or_technique',
        'Objective_of_the_method_within_the_project',
        'Method_maturity',
        'Is_part_of_method',
        'Unique_ID',
        'Method_category',
        'Scale',
        'Documentation',
        'Cost_and_time',
        'Accessibility',
        'Interoperability',
        'Relevance_for_DECODE_use_cases',
        'Applicability_beyond_DECODE',
        'For_Models_Model_requirements',
        'For_Models_Model_assumptions',
        'For_Models_Implementation_details',
        'For_Models_Parameterization_and_validation_incl_accuracy_and_sensitivity_to_inputs',
        'For_Models_Range_of_validity',
        'For_Experimental_Methods_Method_Requirements',
        'For_Experimental_Methods_Method_Assumptions',
        'For_Experimental_Methods_Implementation_details',
        'For_Experimental_Methods_Preparation',
        'For_Experimental_Methods_Validation',
        'For_Experimental_Methods_Range_of_validity',
        'For_Manufacturing_Methods_Process_steps',
        'For_Manufacturing_Methods_Implementation_details',
        'For_Manufacturing_Methods_Validation_and_accuracy_of_the_method',
        'For_Manufacturing_Methods_Range_of_processability',
        'Inputs',
        'Scale_of_inputs',
        'Details_comments_to_Inputs',
        'Outputs',
        'Scale_of_outputs',
        'Details_comments_to_outputs'
    ]

    # Check if all common columns are present
    missing_columns = [col for col in common_columns if col not in df.columns]
    if missing_columns:
        print(f"Missing columns in sheet '{sheet}': {missing_columns}")
        continue  # Skip this sheet if there are missing columns

    # Filter the DataFrame to only include common columns
    df_common = df[common_columns]

    # Drop rows where all columns are NaN (i.e., ignore empty rows)
    df_common = df_common.dropna(how='all')

    # Insert the data into the SQL table
    df_common.to_sql('Methods', conn, if_exists='append', index=False)

# Close the connection to the SQLite database
conn.close()

def query_database(sheet_name, selected_columns=None, search_query=None):
    """ Query the database for all data or specific columns with search capability. """
    conn = sqlite3.connect('methods2.db')
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
