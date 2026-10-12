DROP TABLE IF EXISTS sales;
DROP TABLE IF EXISTS product;
DROP TABLE IF EXISTS cost;
DROP TABLE IF EXISTS competitor_price;
DROP TABLE IF EXISTS inventory;

CREATE TABLE sales (
    order_id TEXT,
    sku TEXT,
    date TEXT,
    qty INTEGER,
    price REAL,
    discount REAL
);

CREATE TABLE product (
    sku TEXT,
    category TEXT,
    season TEXT,
    base_price REAL
);

CREATE TABLE cost (
    sku TEXT,
    cost REAL
);

CREATE TABLE competitor_price (
    sku TEXT,
    date TEXT,
    competitor_price REAL
);

CREATE TABLE inventory (
    sku TEXT,
    date TEXT,
    inventory INTEGER
);