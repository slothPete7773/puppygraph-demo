CREATE DATABASE IF NOT EXISTS customer_domain;
USE customer_domain;
-- 1. Customer Table
CREATE TABLE customer_domain.customer (
  customer_id String,
  first_name String,
  last_name String,
  email String,
  phone String,
  date_of_birth Date,
  registration_date DateTime,
  customer_status String,
  -- 'active', 'inactive', 'suspended'
  loyalty_tier String,
  -- 'bronze', 'silver', 'gold', 'platinum'
  total_lifetime_value Decimal(15, 2),
  created_at DateTime DEFAULT now(),
  updated_at DateTime DEFAULT now()
) ENGINE = MergeTree()
ORDER BY customer_id;
-- Sample data for customer
INSERT INTO customer_domain.customer (
    customer_id,
    first_name,
    last_name,
    email,
    phone,
    date_of_birth,
    registration_date,
    customer_status,
    loyalty_tier,
    total_lifetime_value
  )
VALUES (
    'c001',
    'John',
    'Smith',
    'john.smith@email.com',
    '+1-555-0101',
    '1985-03-15',
    '2023-01-10 10:30:00',
    'active',
    'gold',
    15420.50
  ),
  (
    'c002',
    'Emma',
    'Johnson',
    'emma.j@email.com',
    '+1-555-0102',
    '1990-07-22',
    '2023-02-14 14:20:00',
    'active',
    'platinum',
    28750.00
  ),
  (
    'c003',
    'Michael',
    'Williams',
    'mwilliams@email.com',
    '+1-555-0103',
    '1988-11-30',
    '2023-03-05 09:15:00',
    'active',
    'silver',
    8920.75
  ),
  (
    'c004',
    'Sarah',
    'Brown',
    'sarah.b@email.com',
    '+1-555-0104',
    '1992-05-18',
    '2023-04-20 16:45:00',
    'inactive',
    'bronze',
    2340.00
  ),
  (
    'c005',
    'David',
    'Martinez',
    'dmartinez@email.com',
    '+1-555-0105',
    '1987-09-25',
    '2023-05-12 11:00:00',
    'active',
    'gold',
    19850.25
  );
-- 2. Customer Address Table
CREATE TABLE customer_domain.customer_address (
  address_id String,
  customer_id String,
  address_type String,
  -- 'home', 'work', 'billing', 'shipping'
  street_address String,
  city String,
  state String,
  postal_code String,
  country String,
  is_primary Boolean,
  is_verified Boolean,
  created_at DateTime DEFAULT now(),
  updated_at DateTime DEFAULT now()
) ENGINE = MergeTree()
ORDER BY (customer_id, address_id);
-- Sample data for customer_address
INSERT INTO customer_domain.customer_address (
    address_id,
    customer_id,
    address_type,
    street_address,
    city,
    state,
    postal_code,
    country,
    is_primary,
    is_verified
  )
VALUES (
    'a001',
    'c001',
    'home',
    '123 Main St',
    'New York',
    'NY',
    '10001',
    'USA',
    true,
    true
  ),
  (
    'a002',
    'c001',
    'work',
    '456 Business Ave',
    'New York',
    'NY',
    '10002',
    'USA',
    false,
    true
  ),
  (
    'a003',
    'c002',
    'home',
    '789 Oak Drive',
    'Los Angeles',
    'CA',
    '90001',
    'USA',
    true,
    true
  ),
  (
    'a004',
    'c002',
    'shipping',
    '321 Elm Street',
    'San Francisco',
    'CA',
    '94102',
    'USA',
    false,
    true
  ),
  (
    'a005',
    'c003',
    'home',
    '555 Pine Road',
    'Chicago',
    'IL',
    '60601',
    'USA',
    true,
    true
  ),
  (
    'a006',
    'c004',
    'home',
    '888 Maple Lane',
    'Houston',
    'TX',
    '77001',
    'USA',
    true,
    false
  ),
  (
    'a007',
    'c005',
    'home',
    '999 Cedar Court',
    'Phoenix',
    'AZ',
    '85001',
    'USA',
    true,
    true
  ),
  (
    'a008',
    'c005',
    'billing',
    '111 Birch Blvd',
    'Phoenix',
    'AZ',
    '85002',
    'USA',
    false,
    true
  );
-- 3. Customer Transaction Table
CREATE TABLE customer_domain.customer_transaction (
  transaction_id String,
  customer_id String,
  transaction_date DateTime,
  transaction_type String,
  -- 'purchase', 'refund', 'payment', 'adjustment'
  amount Decimal(15, 2),
  currency String,
  payment_method String,
  -- 'credit_card', 'debit_card', 'paypal', 'bank_transfer', 'cash'
  status String,
  -- 'completed', 'pending', 'failed', 'cancelled'
  order_id String,
  description String,
  created_at DateTime DEFAULT now()
) ENGINE = MergeTree()
ORDER BY (customer_id, transaction_date);
-- Sample data for customer_transaction
INSERT INTO customer_domain.customer_transaction (
    transaction_id,
    customer_id,
    transaction_date,
    transaction_type,
    amount,
    currency,
    payment_method,
    status,
    order_id,
    description
  )
VALUES (
    't001',
    'c001',
    '2025-01-15 10:30:00',
    'purchase',
    250.00,
    'USD',
    'credit_card',
    'completed',
    'ord-001',
    'Electronics purchase'
  ),
  (
    't002',
    'c001',
    '2025-02-20 14:15:00',
    'purchase',
    450.50,
    'USD',
    'credit_card',
    'completed',
    'ord-002',
    'Home appliances'
  ),
  (
    't003',
    'c001',
    '2025-03-10 09:45:00',
    'refund',
    -50.00,
    'USD',
    'credit_card',
    'completed',
    'ord-002',
    'Partial refund'
  ),
  (
    't004',
    'c002',
    '2025-01-22 16:20:00',
    'purchase',
    1200.00,
    'USD',
    'paypal',
    'completed',
    'ord-003',
    'Laptop purchase'
  ),
  (
    't005',
    'c002',
    '2025-02-14 11:00:00',
    'purchase',
    850.00,
    'USD',
    'credit_card',
    'completed',
    'ord-004',
    'Furniture'
  ),
  (
    't006',
    'c002',
    '2025-03-05 13:30:00',
    'purchase',
    320.75,
    'USD',
    'debit_card',
    'completed',
    'ord-005',
    'Clothing'
  ),
  (
    't007',
    'c003',
    '2025-01-30 10:00:00',
    'purchase',
    175.25,
    'USD',
    'bank_transfer',
    'completed',
    'ord-006',
    'Books'
  ),
  (
    't008',
    'c003',
    '2025-02-28 15:45:00',
    'purchase',
    95.00,
    'USD',
    'credit_card',
    'completed',
    'ord-007',
    'Software subscription'
  ),
  (
    't009',
    'c004',
    '2025-01-18 12:30:00',
    'purchase',
    80.00,
    'USD',
    'cash',
    'completed',
    'ord-008',
    'Office supplies'
  ),
  (
    't010',
    'c004',
    '2025-02-25 09:15:00',
    'purchase',
    45.00,
    'USD',
    'debit_card',
    'failed',
    'ord-009',
    'Payment declined'
  ),
  (
    't011',
    'c005',
    '2025-01-12 14:00:00',
    'purchase',
    680.00,
    'USD',
    'credit_card',
    'completed',
    'ord-010',
    'Sports equipment'
  ),
  (
    't012',
    'c005',
    '2025-02-08 11:30:00',
    'purchase',
    920.50,
    'USD',
    'paypal',
    'completed',
    'ord-011',
    'Camera gear'
  ),
  (
    't013',
    'c005',
    '2025-03-15 16:00:00',
    'purchase',
    510.25,
    'USD',
    'credit_card',
    'pending',
    'ord-012',
    'Pending shipment'
  );