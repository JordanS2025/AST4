#Jordan, David & Eli 
# AST4 : PostgreSQL Database 
import psycopg2
from psycopg2 import sql

# Connecting to the database
try:
    connection = psycopg2.connect(
        dbname="AST4",
        user="postgres",
        password="Entimeo09",
        host="localhost",
        port="5432"
    )
    print("Connected to database successfully.")
except psycopg2.Error as e:
    print("Error connecting to database:", e)
    exit(1)  # Exit if connection fails

cursor = connection.cursor()

# Function to check if table exists and create if it does not
def check_and_create_table(table_name, create_table_sql):
    cursor.execute("SELECT EXISTS(SELECT 1 FROM pg_tables WHERE tablename=%s);", (table_name,))
    if cursor.fetchone()[0]:
        print(f"Table {table_name} already exists.")
    else:
        cursor.execute(create_table_sql)
        print(f"Table {table_name} created successfully.")

# Function to insert data into a specified table
def insert_data(cursor, table_name, data_dict):
    columns = data_dict.keys()
    values = [data_dict[column] for column in columns]
    query = sql.SQL("INSERT INTO {table} ({fields}) VALUES ({values}) ON CONFLICT DO NOTHING").format(
        table=sql.Identifier(table_name),
        fields=sql.SQL(', ').join(map(sql.Identifier, columns)),
        values=sql.SQL(', ').join(sql.Placeholder() * len(values))
    )
    try:
        cursor.execute(query, values)
        print(f"Data inserted successfully into {table_name}.")
    except psycopg2.Error as e:
        print(f"An error occurred: {e}")

# Define the CREATE TABLE statements
create_table_query_function = '''
CREATE TABLE "function" (
    function_name VARCHAR(255),
    api_name VARCHAR(255),
    PRIMARY KEY (function_name, api_name),
    UNIQUE (function_name),
    FOREIGN KEY (api_name) REFERENCES "API"(api_name)
);
'''

create_table_query_api_function = '''
CREATE TABLE "API_function_specific" (
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
check_and_create_table('function', create_table_query_function)
check_and_create_table('API_function_specific', create_table_query_api_function)

# Example data for 'function' table
function_data = {
    'function_name': 'CalculateAverage',
    'api_name': 'MathAPI'
}
insert_data(cursor, 'function', function_data)

# Example data for 'API_function_specific' table
api_function_data = {
    'api_name_fk': 'MathAPI',
    'function_name_fk': 'CalculateAverage',
    'api_context': 'Used for statistical calculations',
    'api_topic': 'Mathematics',
    'function_context': 'Calculate the mean of given numbers',
    'function_topic': 'Statistics',
    'llm_expert_API': 'Yes',
    'sim_expert_API': 0.95,
    'llm_expert_function': 'Yes',
    'sim_expert_function': 0.90
}
insert_data(cursor, 'API_function_specific', api_function_data)

# Commit the transaction and close the connection
connection.commit()
cursor.close()
connection.close()
