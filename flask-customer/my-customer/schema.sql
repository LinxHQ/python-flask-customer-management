DROP TABLE IF EXISTS customer;
DROP TABLE IF EXISTS invoice;

CREATE TABLE customer (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT UNIQUE NOT NULL,
  full_address TEXT,
  phone_1 VARCHAR(100),
  phone_2 VARCHAR(100),
  email VARCHAR(100),
  website VARCHAR(100),
  remark TEXT
);

CREATE TABLE invoice (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  customer_id INTEGER NOT NULL,
  invoice_date DATE,
  description TEXT NOT NULL,
  sub_total FLOAT,
  discount FLOAT,
  tax FLOAT,
  FOREIGN KEY (customer_id) REFERENCES customer (id)
);