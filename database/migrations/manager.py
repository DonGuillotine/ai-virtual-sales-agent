import os
import logging
from pathlib import Path
import sqlite3
import re
from typing import List, Tuple

from database.db_manager import DatabaseManager

logger = logging.getLogger(__name__)

class MigrationManager:
    """Manages database migrations to evolve the schema over time."""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.migrations_dir = Path(os.path.dirname(__file__)) / "versions"
        self._ensure_migration_table()
    
    def _ensure_migration_table(self) -> None:
        """Creates the migration tracking table if it doesn't exist."""
        with self.db_manager.get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS schema_migrations (
                    version INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
    
    def get_applied_migrations(self) -> List[int]:
        """Returns a list of already applied migration versions."""
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT version FROM schema_migrations ORDER BY version")
            return [row['version'] for row in cursor.fetchall()]
    
    def get_available_migrations(self) -> List[Tuple[int, str, str]]:
        """Returns a list of available migrations from the versions directory."""
        migrations = []
        
        if not self.migrations_dir.exists():
            return migrations
        
        for file_path in sorted(self.migrations_dir.glob("*.sql")):
            # Extract version number from filename (e.g., 001_initial_schema.sql -> 1)
            filename = file_path.name
            match = re.match(r'^(\d+)_(.+)\.sql$', filename)
            if match:
                version = int(match.group(1))
                name = match.group(2)
                with open(file_path, 'r') as f:
                    content = f.read()
                migrations.append((version, name, content))
        
        return migrations
    
    def get_pending_migrations(self) -> List[Tuple[int, str, str]]:
        """Returns a list of migrations that haven't been applied yet."""
        applied = set(self.get_applied_migrations())
        return [(v, n, c) for v, n, c in self.get_available_migrations() if v not in applied]
    
    def apply_migration(self, version: int, name: str, content: str) -> bool:
        """Applies a single migration to the database."""
        try:
            with self.db_manager.get_connection() as conn:
                # Start transaction
                conn.execute("BEGIN TRANSACTION")
                
                # Apply the migration
                conn.executescript(content)
                
                # Record the migration
                conn.execute(
                    "INSERT INTO schema_migrations (version, name) VALUES (?, ?)",
                    (version, name)
                )
                
                # Commit the transaction
                conn.execute("COMMIT")
                
            logger.info(f"Applied migration {version}: {name}")
            return True
            
        except sqlite3.Error as e:
            logger.error(f"Failed to apply migration {version}: {e}")
            return False
    
    def run_migrations(self) -> bool:
        """Runs all pending migrations in order."""
        pending = self.get_pending_migrations()
        
        if not pending:
            logger.info("No pending migrations to apply")
            return True
        
        logger.info(f"Found {len(pending)} pending migrations")
        
        success = True
        for version, name, content in pending:
            if not self.apply_migration(version, name, content):
                success = False
                break
        
        if success:
            logger.info("All migrations applied successfully")
        else:
            logger.error("Migration process failed")
            
        return success