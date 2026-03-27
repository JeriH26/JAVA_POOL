-- =============================================================
-- TCXR Homework 1: SQL and Data Lineage
-- setup.sql
--
-- This file reproduces both table schemas from the homework
-- problem and inserts sample data so every task can be run
-- and verified directly in PostgreSQL. 
-- (Please see the README for Answers details.)
--
-- Usage:
--   psql -U <your_user> -d <your_database> -f setup.sql
-- =============================================================


-- ---------------------------------------------------------------
-- 0. Clean up from any previous run
-- ---------------------------------------------------------------
DROP TABLE IF EXISTS transformed_products;
DROP TABLE IF EXISTS raw_products;


-- ---------------------------------------------------------------
-- 1. Original / raw table
--    Mirrors the schema given in the problem statement.
--    price and cost are in Japanese Yen (¥).
-- ---------------------------------------------------------------
CREATE TABLE raw_products (
    product_id       INT           PRIMARY KEY,
    product_name     VARCHAR(255)  NOT NULL,
    warehouse        VARCHAR(20)   NOT NULL,   -- e.g. "W8475839"
    store            VARCHAR(255)  NOT NULL,
    price            FLOAT         NOT NULL,   -- selling price (¥)
    cost             FLOAT         NOT NULL,   -- manufacturing cost (¥)
    date_sold        TIMESTAMP     NOT NULL,   -- full datetime
    date_manufactured TIMESTAMP   NOT NULL    -- full datetime
);


-- ---------------------------------------------------------------
-- 2. Fake Sample data for raw_products, for easy testing and verification.
-- ---------------------------------------------------------------
INSERT INTO raw_products VALUES
(1001, 'Mountain Bike',   'W8475839', 'Tokyo Central Store',    45000.00, 28000.00, '2024-03-15 10:23:45', '2024-01-10 08:00:00'),
(1002, 'Mountain Bike',   'L5749302', 'Osaka West Store',       45000.00, 28000.00, '2024-03-15 14:05:12', '2024-01-12 09:30:00'),
(1003, 'Road Bike',       'W8475839', 'Tokyo Central Store',    62000.00, 39000.00, '2024-04-02 09:11:33', '2024-02-01 07:45:00'),
(1004, 'Helmet Pro',      'K3820194', 'Nagoya East Store',       8500.00,  4200.00, '2024-04-10 16:44:00', '2024-03-05 11:00:00'),
(1005, 'Cycling Gloves',  'L5749302', 'Osaka West Store',        3200.00,  1500.00, '2024-04-11 11:30:00', '2024-03-08 13:15:00'),
(1006, 'Bicycle Lock',    'W8475839', 'Sapporo North Store',     2800.00,  1100.00, '2024-04-20 08:00:00', '2024-03-20 10:00:00'),
(1007, 'Electric Bike',   'M9012345', 'Fukuoka South Store',   120000.00, 85000.00, '2024-05-01 15:22:00', '2024-02-28 06:30:00'),
(1008, 'Electric Bike',   'M9012345', 'Tokyo Central Store',   120000.00, 85000.00, '2024-05-03 10:10:00', '2024-03-01 06:30:00');


-- ---------------------------------------------------------------
-- 3. Transformed table — analyst's revised schema
--    Changes applied:
--      - product_name   : DROPPED
--      - warehouse      : SPLIT into warehouse_letter (CHAR(1))
--                         and warehouse_num_id (INT)
--      - date_sold      : TIMESTAMP -> DATE  (undisclosed change)
--      - date_manufactured: TIMESTAMP -> DATE (undisclosed change)
--      - price comment  : labelled as Japanese Yen (no type change)
-- ---------------------------------------------------------------
CREATE TABLE transformed_products (
    product_id          INT         PRIMARY KEY,
    -- product_name removed by analyst
    warehouse_letter    CHAR(1)     NOT NULL,   -- e.g. 'W'
    warehouse_num_id    INT         NOT NULL,   -- e.g. 8475839
    store               VARCHAR(255) NOT NULL,
    price               FLOAT       NOT NULL,   -- selling price (¥ JPY)
    cost                FLOAT       NOT NULL,   -- manufacturing cost (¥ JPY)
    date_sold           DATE        NOT NULL,   -- TIME portion silently lost
    date_manufactured   DATE        NOT NULL    -- TIME portion silently lost
);


-- ---------------------------------------------------------------
-- 4. Populate transformed_products from raw_products
--    This mirrors what the analyst would have done.
--
--    NOTE: SUBSTRING(warehouse, 1, 1)        -> warehouse_letter
--          SUBSTRING(warehouse, 2)::INT       -> warehouse_num_id
--          date_sold::DATE                    -> loses time component
-- ---------------------------------------------------------------
INSERT INTO transformed_products
SELECT
    product_id,
    SUBSTRING(warehouse, 1, 1)           AS warehouse_letter,
    SUBSTRING(warehouse, 2)::INT         AS warehouse_num_id,
    store,
    price,
    cost,
    date_sold::DATE                      AS date_sold,
    date_manufactured::DATE              AS date_manufactured
FROM raw_products;


-- ---------------------------------------------------------------
-- 5. Task 3 — Reconstruct the warehouse column
--
--    Simple version (no zero-padding guarantee):
--      CONCAT(warehouse_letter, warehouse_num_id)
--
--    Safe version (preserves original 7-digit format):
--      CONCAT(warehouse_letter, LPAD(warehouse_num_id::TEXT, 7, '0'))
-- ---------------------------------------------------------------

-- Simple reconstruction
SELECT
    product_id,
    CONCAT(warehouse_letter, warehouse_num_id)                         AS warehouse_simple,
    CONCAT(warehouse_letter, LPAD(warehouse_num_id::TEXT, 7, '0'))     AS warehouse_padded,
    store,
    price,
    cost,
    date_sold,
    date_manufactured
FROM transformed_products;


-- ---------------------------------------------------------------
-- 6. Verification queries
--    Run these to inspect the data and spot the analyst's issues.
-- ---------------------------------------------------------------

-- 6a. Compare raw vs transformed row counts (should match)
SELECT
    (SELECT COUNT(*) FROM raw_products)         AS raw_count,
    (SELECT COUNT(*) FROM transformed_products) AS transformed_count;

-- 6b. Show time information lost in the date conversion
SELECT
    r.product_id,
    r.date_sold                       AS original_datetime,
    t.date_sold                       AS transformed_date,
    r.date_sold::DATE = t.date_sold   AS dates_match,
    r.date_sold::TIME                 AS time_lost
FROM raw_products r
JOIN transformed_products t USING (product_id)
ORDER BY r.product_id;

-- 6c. Demonstrate that two sales on the same day (product 1001 & 1002)
--     are now indistinguishable by warehouse + date alone
SELECT
    t.product_id,
    CONCAT(t.warehouse_letter, LPAD(t.warehouse_num_id::TEXT, 7, '0')) AS warehouse,
    t.store,
    t.date_sold
FROM transformed_products t
ORDER BY t.date_sold, warehouse;

-- 6d. Show that product_name context is now completely lost
SELECT
    r.product_id,
    r.product_name,
    'NOT AVAILABLE in transformed_products' AS product_name_in_transformed
FROM raw_products r
ORDER BY r.product_id;
