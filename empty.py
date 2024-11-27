import sqlite3

# Connect to the SQLite database (change 'your_database.db' to your actual database file)
conn = sqlite3.connect('KnowledgeBase.db')
cursor = conn.cursor()

# SQL query to delete all records from the table (replace 'your_table_name' with the actual table name)
cursor.execute('DELETE FROM mapCreationTable')

# Commit the transaction to save changes
conn.commit()

# Optionally, check if the table is now empty
cursor.execute('SELECT COUNT(*) FROM mapCreationTable')
count = cursor.fetchone()[0]
print(f"Total records after deletion: {count}")

# Close the connection
conn.close()
