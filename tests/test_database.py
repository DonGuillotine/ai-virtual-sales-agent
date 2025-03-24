import unittest
import os
import tempfile
import shutil
from pathlib import Path

from database.db_manager import DatabaseManager
from database.config import DatabaseConfig


class TestDatabaseManager(unittest.TestCase):
    """Test cases for the DatabaseManager class."""

    def setUp(self):
        """Set up a temporary database for testing."""
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = Path(self.temp_dir) / "test_store.db"
        self.schema_path = Path("database/db/schemas.sql")
        self.products_path = Path("database/db/products.json")
        
        self.config = DatabaseConfig(
            db_name="test_store.db",
            db_path=str(self.db_path),
            schema_path=str(self.schema_path),
            products_path=str(self.products_path),
        )
        
        self.db_manager = DatabaseManager(self.config)

    def tearDown(self):
        """Clean up the temporary directory."""
        shutil.rmtree(self.temp_dir)

    def test_create_database(self):
        """Test database creation."""
        result = self.db_manager.create_database()
        self.assertTrue(result)
        self.assertTrue(self.db_path.exists())

    def test_insert_product(self):
        """Test inserting a single product."""
        self.db_manager.create_database()
        
        result = self.db_manager.insert_product(
            product_name="Test Product",
            category="Test Category",
            description="Test Description",
            price=99.99,
            quantity=10
        )
        self.assertTrue(result)
        
        # Verify the product was inserted
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM products WHERE ProductName = ?", ("test product",))
            product = cursor.fetchone()
            
            self.assertIsNotNone(product)
            self.assertEqual(product["ProductName"], "test product")
            self.assertEqual(product["Category"], "test category")
            self.assertEqual(product["Description"], "Test Description")
            self.assertEqual(float(product["Price"]), 99.99)
            self.assertEqual(product["Quantity"], 10)

    def test_insert_products_from_json(self):
        """Test inserting products from JSON file."""
        self.db_manager.create_database()
        result = self.db_manager.insert_products_from_json()
        self.assertTrue(result)
        
        # Verify products were inserted
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) as count FROM products")
            count = cursor.fetchone()["count"]
            self.assertGreater(count, 0)


if __name__ == '__main__':
    unittest.main()