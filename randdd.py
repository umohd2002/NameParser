import sqlite3
import os

def optimize_database(db_path):
    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Display the initial size of the database
        initial_size = os.path.getsize(db_path)
        print(f"Initial database size: {initial_size / (1024 * 1024):.2f} MB")

        # Perform VACUUM to rebuild the database and remove unused space
        print("Running VACUUM...")
        cursor.execute("VACUUM;")
        conn.commit()

        # List all indexes and identify unused ones
        cursor.execute("SELECT name, tbl_name FROM sqlite_master WHERE type='index';")
        indexes = cursor.fetchall()
        print(f"Found {len(indexes)} indexes.")
        for index_name, table_name in indexes:
            # Check if the index is being used (you may implement custom logic here)
            print(f"Index: {index_name} on Table: {table_name}")
            # Uncomment to drop an unused index
            # cursor.execute(f"DROP INDEX {index_name};")
        
        # Check for temporary or large tables and drop them if not needed
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        for table_name, in tables:
            # Example: Delete from temporary tables (customize as needed)
            if table_name.startswith("temp_"):
                print(f"Deleting temporary table: {table_name}")
                cursor.execute(f"DROP TABLE {table_name};")
        
        conn.commit()

        # Display the final size of the database
        final_size = os.path.getsize(db_path)
        print(f"Final database size: {final_size / (1024 * 1024):.2f} MB")
        print(f"Space saved: {(initial_size - final_size) / (1024 * 1024):.2f} MB")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

# Path to your database file
db_path = 'KnowledgeBase.db'

# Run the optimization
optimize_database(db_path)
