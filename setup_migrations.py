import os
import shutil
from pathlib import Path

def setup_migrations():
    """Sets up the migrations directory structure and copies the initial schema."""
    
    # Create migrations directory structure
    migrations_dir = Path("database/migrations")
    versions_dir = migrations_dir / "versions"
    
    migrations_dir.mkdir(exist_ok=True)
    versions_dir.mkdir(exist_ok=True)
    
    # Proper __init__.py files to avoid circular imports
    with open(migrations_dir / "__init__.py", 'w') as f:
        f.write("# Migrations package\n")
    
    with open(versions_dir / "__init__.py", 'w') as f:
        f.write("# Migration versions package\n")
    
    # Copy schema.sql to initial migration if it doesn't exist
    initial_migration_path = versions_dir / "001_initial_schema.sql"
    
    if not initial_migration_path.exists():
        schema_path = Path("database/db/schemas.sql")
        if schema_path.exists():
            # Copy with header comment
            with open(schema_path, 'r') as src_file:
                schema_content = src_file.read()
            
            with open(initial_migration_path, 'w') as dest_file:
                dest_file.write("-- This is the initial schema migration\n")
                dest_file.write("-- It creates the base tables for the application\n\n")
                dest_file.write(schema_content)
            
            print(f"Created initial migration from {schema_path}")
        else:
            print(f"Warning: Schema file {schema_path} does not exist")
    
    print("Migration system setup complete!")

if __name__ == "__main__":
    setup_migrations()
