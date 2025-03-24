import os
import sqlite3
from database.db_manager import DatabaseManager

def reset_database():
    """Reset the database by deleting it and recreating it with fresh data."""
    db_path = "database/db/store.db"
    
    # Delete existing database if it exists
    if os.path.exists(db_path):
        try:
            os.remove(db_path)
            print(f"Deleted existing database: {db_path}")
        except Exception as e:
            print(f"Error deleting database: {e}")
            return False
    
    # Create a new database with fresh data
    db_manager = DatabaseManager()
    if not db_manager.create_database():
        print("Failed to create database")
        return False
    
    # Run migrations
    if not db_manager.run_migrations():
        print("Failed to apply migrations")
        return False
    
    # Insert products data
    if db_manager.config.products_path:
        if not db_manager.insert_products_from_json():
            print("Failed to insert products")
            return False
    
    print("Database reset successfully!")
    return True

if __name__ == "__main__":
    reset_database()