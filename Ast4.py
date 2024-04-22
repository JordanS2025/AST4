#Jordan, David & Eli 
# AST4 : PostgreSQL Database 
import psycopg2
import json

# Load JSON data from a file
def load_json_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Convert JSON keys to lowercase to match the database column names
def convert_keys_to_lowercase(data):
    return {k.lower(): v for k, v in data.items()}

# Function to insert data into a specified table
def insert_data(cursor, table_name, data_dict):
    data_dict = convert_keys_to_lowercase(data_dict)  # Convert keys to lowercase
    columns = data_dict.keys()
    values = [data_dict[column] for column in columns]
    placeholders = ', '.join(['%s'] * len(values))
    column_identifiers = ', '.join([f'"{column}"' for column in columns])  # Keep the double quotes
    insert_query = f'INSERT INTO "{table_name}" ({column_identifiers}) VALUES ({placeholders}) ON CONFLICT DO NOTHING'
    cursor.execute(insert_query, values)
    print(f"Data inserted successfully into {table_name}.")

# Connect to the database
try:
    # Adjust the following credentials to your database configuration
    connection = psycopg2.connect(
        dbname="AST4",
        user="postgres",
        password="Entimeo09",
        host="localhost",
        port="5432"
    )
    connection.autocommit = False
    cursor = connection.cursor()

    # Load JSON data
    json_data = load_json_data('data.json')

    # Insert data into 'API' table
    for item in json_data['API']:
        insert_data(cursor, 'API', item)

    # Insert data into 'function' table
    for item in json_data['function']:
        insert_data(cursor, 'function', item)

    # Insert data into 'API_function_specific' table
    for item in json_data['API_function_specific']:
        insert_data(cursor, 'API_function_specific', item)

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
