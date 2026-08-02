CREATE TABLE inventory_category (
    id SERIAL PRIMARY KEY,
    parent_id INTEGER REFERENCES inventory_category(id) ON DELETE RESTRICT,
    name VARCHAR(50) UNIQUE NOT NULL,
    slug VARCHAR(55) UNIQUE NOT NULL,
    is_active BOOLEAN DEFAULT FALSE,
    level SMALLINT DEFAULT 0
);

CREATE TABLE inventory_promotionevent (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP NOT NULL,
    price_reduction INTEGER NOT NULL
);

CREATE TABLE inventory_product (
    id SERIAL PRIMARY KEY,
    category_id INTEGER NOT NULL REFERENCES inventory_category(id) ON DELETE CASCADE,
    name VARCHAR(50) UNIQUE NOT NULL,
    slug VARCHAR(55) UNIQUE NOT NULL,
    description TEXT,
    is_digital BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    price NUMERIC(10, 2) NOT NULL
);

CREATE TABLE inventory_productpromotionevent (
    id SERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES inventory_product(id) ON DELETE CASCADE,
    promotion_event_id INTEGER NOT NULL REFERENCES inventory_promotionevent(id) ON DELETE CASCADE,
    UNIQUE (product_id, promotion_event_id)
);

CREATE TABLE inventory_stockmanagement (
    id SERIAL PRIMARY KEY,
    product_id INTEGER UNIQUE NOT NULL REFERENCES inventory_product(id) ON DELETE CASCADE,
    quantity INTEGER DEFAULT 0,
    last_checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE inventory_user (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(60) NOT NULL
);

CREATE TABLE inventory_order (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES inventory_user(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE inventory_orderproduct (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES inventory_order(id) ON DELETE CASCADE,
    product_id INTEGER NOT NULL REFERENCES inventory_product(id) ON DELETE CASCADE,
    quantity INTEGER NOT NULL,
    UNIQUE (product_id, order_id)
);


-- Load data into tables with correct table names
COPY inventory_category (id, parent_id, name, slug, is_active, level)
FROM '/data/category.csv'
DELIMITER ','
CSV HEADER;

COPY inventory_promotionevent (id, name, start_date, end_date, price_reduction)
FROM '/data/promotionevent.csv'
DELIMITER ','
CSV HEADER;

COPY inventory_product (id, category_id, name, slug, description, is_digital, is_active, created_at, updated_at, price)
FROM '/data/product.csv'
DELIMITER ','
CSV HEADER;

COPY inventory_productpromotionevent (id, product_id, promotion_event_id)
FROM '/data/productpromotionevent.csv'
DELIMITER ','
CSV HEADER;

COPY inventory_stockmanagement (id, product_id, quantity, last_checked_at)
FROM '/data/stockmanagement.csv'
DELIMITER ','
CSV HEADER;

COPY inventory_user (id, username, email, password)
FROM '/data/user.csv'
DELIMITER ','
CSV HEADER;

COPY inventory_order (id, user_id, created_at, updated_at)
FROM '/data/order.csv'
DELIMITER ','
CSV HEADER;

COPY inventory_orderproduct (id, order_id, product_id, quantity)
FROM '/data/orderproduct.csv'
DELIMITER ','
CSV HEADER;
