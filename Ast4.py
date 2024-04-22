#Jordan, David & Eli 
# AST4 : PostgreSQL Database 
import psycopg2
from psycopg2 import sql

# Function to check if table exists and create if it does not
def check_and_create_table(cursor, table_name, create_table_sql):
    cursor.execute("SELECT EXISTS(SELECT 1 FROM pg_tables WHERE tablename=%s);", (table_name,))
    exists = cursor.fetchone()[0]
    if not exists:
        cursor.execute(create_table_sql)
        print(f"Table {table_name} created successfully.")
    else:
        print(f"Table {table_name} already exists.")

# Function to insert data into a specified table
def insert_data(cursor, table_name, data_dict):
    columns = data_dict.keys()
    values = [data_dict[column] for column in columns]
    placeholders = ', '.join(['%s'] * len(values))
    column_identifiers = ', '.join(map(lambda c: f'"{c}"', columns))
    insert_query = f'INSERT INTO "{table_name}" ({column_identifiers}) VALUES ({placeholders}) ON CONFLICT DO NOTHING'
    cursor.execute(insert_query, values)
    print(f"Data inserted successfully into {table_name}.")

# Connect to the database
try:
    connection = psycopg2.connect(
        dbname="AST4",
        user="postgres",
        password="Entimeo09",
        host="localhost",
        port="5432"
    )
    connection.autocommit = False
    cursor = connection.cursor()
    print("Connected to database successfully.")

    # Define the CREATE TABLE statements
    # Make sure these statements match the actual desired structure
    create_table_query_api = '''
    CREATE TABLE IF NOT EXISTS "API" (
        api_name VARCHAR(255) PRIMARY KEY,
        class VARCHAR(255),
        count INTEGER,
        expert BOOLEAN
    );
    '''
    
    create_table_query_function = '''
    CREATE TABLE IF NOT EXISTS "function" (
        function_name VARCHAR(255),
        api_name VARCHAR(255),
        PRIMARY KEY (function_name, api_name),
        UNIQUE (function_name),
        FOREIGN KEY (api_name) REFERENCES "API"(api_name)
    );
    '''

    create_table_query_api_function = '''
    CREATE TABLE IF NOT EXISTS "API_function_specific" (
        api_name_fk VARCHAR(255),
        function_name_fk VARCHAR(255),
        api_context TEXT,
        api_topic VARCHAR(255),
        function_context TEXT,
        function_topic VARCHAR(255),
        llm_expert_API VARCHAR(255),
        sim_expert_API FLOAT,
        llm_expert_function VARCHAR(255),
        sim_expert_function FLOAT,
        PRIMARY KEY (api_name_fk, function_name_fk),
        FOREIGN KEY (api_name_fk) REFERENCES "API"(api_name),
        FOREIGN KEY (function_name_fk) REFERENCES "function"(function_name)
    );
    '''

    # Check and create tables
    check_and_create_table(cursor, 'API', create_table_query_api)
    check_and_create_table(cursor, 'function', create_table_query_function)
    check_and_create_table(cursor, 'API_function_specific', create_table_query_api_function)
    
    # Example data for 'API' table
    api_data = {
        'api_name': 'MathAPI',
        'class': 'Math',
        'count': 0,
        'expert': True
    }
    
    # Insert data into 'API' table if 'MathAPI' doesn't exist
    cursor.execute("SELECT COUNT(*) FROM \"API\" WHERE api_name = 'MathAPI';")
    if cursor.fetchone()[0] == 0:
        insert_data(cursor, 'API', api_data)

    # Example data for 'function' table
    function_data = {
        'function_name': 'CalculateAverage',
        'api_name': 'MathAPI'
    }
    insert_data(cursor, 'function', function_data)

    # Example data for 'API_function_specific' table
    # Example data for 'API_function_specific' table
# Example data for 'API_function_specific' table
    api_function_data = {
    'api_name_fk': 'MathAPI',
    'function_name_fk': 'CalculateAverage',
    'api_context': 'Used for statistical calculations',
    'api_topic': 'Mathematics',
    'function_context': 'Calculate the mean of given numbers',
    'function_topic': 'Statistics',
    'llm_expert_api': 'Yes',  # Corrected to lowercase
    'sim_expert_api': 0.95,   # Corrected to lowercase
    'llm_expert_function': 'Yes',  # Ensure this is also correct
    'sim_expert_function': 0.90    # Ensure this is also correct
    }

    insert_data(cursor, 'API_function_specific', api_function_data)

    # Commit the transaction
    connection.commit()

except psycopg2.Error as e:
    print(f"An error occurred: {e}")
    if connection:
        connection.rollback()

finally:
    if cursor:
        cursor.close()
    if connection:
        connection.close()
