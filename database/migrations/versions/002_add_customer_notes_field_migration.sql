ALTER TABLE orders ADD COLUMN customer_notes TEXT;

CREATE INDEX idx_product_name ON products(ProductName);
CREATE INDEX idx_product_category ON products(Category);