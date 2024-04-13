#Jordan, David & Eli 
# AST4 : PostgreSQL Database 
import psycopg2

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

 # Define the CREATE TABLE statement
create_table_query = '''
CREATE TABLE "function" (
    function_name VARCHAR(255),
    api_name VARCHAR(255),
    PRIMARY KEY (function_name, api_name),
    UNIQUE (function_name),  -- Add a unique constraint
    FOREIGN KEY (api_name) REFERENCES "API"(api_name)
);
'''

 
create_table_query_function = '''
CREATE TABLE API_function_specific (
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
    FOREIGN KEY (function_name_fk) REFERENCES function(function_name)
);
'''

# Allows us to excute the query
cursor = connection.cursor()


# Execute the CREATE TABLE statement
cursor.execute(create_table_query)
cursor.execute(create_table_query_function)

 # Commit the transaction
connection.commit()
print("Table created successfully.")

# closing database 
cursor.close()
connection.close()
