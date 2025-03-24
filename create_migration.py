import os
import sys
from pathlib import Path
import re
import datetime

def create_migration(name):
    """Creates a new migration file with the given name."""
    if not name:
        print("Error: Migration name is required")
        print("Usage: python create_migration.py <migration_name>")
        return False
    
    # Sanitize name
    name = re.sub(r'[^a-zA-Z0-9_]', '_', name.lower())
    
    # Find the next version number
    migrations_dir = Path("database/migrations/versions")
    if not migrations_dir.exists():
        print(f"Error: Migrations directory not found at {migrations_dir}")
        print("Run setup_migrations.py first")
        return False
    
    existing_migrations = list(migrations_dir.glob("*.sql"))
    if not existing_migrations:
        next_version = 1
    else:
        versions = []
        for path in existing_migrations:
            match = re.match(r'^(\d+)_', path.name)
            if match:
                versions.append(int(match.group(1)))
        
        next_version = max(versions) + 1 if versions else 1
    
    # Create the migration file
    version_str = f"{next_version:03d}"
    filename = f"{version_str}_{name}.sql"
    filepath = migrations_dir / filename
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(filepath, 'w') as f:
        f.write(f"-- Migration: {name}\n")
        f.write(f"-- Created: {timestamp}\n\n")
        f.write("-- Write your migration SQL here\n\n")
    
    print(f"Created new migration: {filepath}")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Error: Migration name is required")
        print("Usage: python create_migration.py <migration_name>")
        sys.exit(1)
    
    migration_name = sys.argv[1]
    create_migration(migration_name)