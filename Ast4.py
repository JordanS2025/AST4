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

# Allows us to excute the query
cursor = connection.cursor()

cursor.execute('SELECT * FROM "public"."API"')

rows = cursor.fetchall()
for row in rows:
    print(row[0])

# closing database 
cursor.close()
connection.close()
