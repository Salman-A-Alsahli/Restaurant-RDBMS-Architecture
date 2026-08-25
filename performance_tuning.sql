-- =============================================================
-- Performance Tuning for Restaurant PostgreSQL Database
-- =============================================================
-- Purpose:
--   Demonstrate realistic database performance analysis on large
--   tables such as person_order, hasordercook, person, and chef.
--   Show potential query bottlenecks, effective indexing, and the
--   impact of a targeted B-Tree index using EXPLAIN ANALYZE.
-- =============================================================

-- -------------------------------------------------------------
-- 1. Inspect table sizes and growth
-- -------------------------------------------------------------
SELECT
    'person' AS table_name,
    COUNT(*) AS row_count
FROM person
UNION ALL
SELECT
    'person_order' AS table_name,
    COUNT(*) AS row_count
FROM person_order
UNION ALL
SELECT
    'hasordercook' AS table_name,
    COUNT(*) AS row_count
FROM hasordercook
UNION ALL
SELECT
    'chef' AS table_name,
    COUNT(*) AS row_count
FROM chef
UNION ALL
SELECT
    'customer' AS table_name,
    COUNT(*) AS row_count
FROM customer
ORDER BY table_name;

-- -------------------------------------------------------------
-- 2. Query that is likely to scan large tables inefficiently
-- -------------------------------------------------------------
-- This query joins a large fact table with customer information and
-- filters using a non-indexed column pattern.
EXPLAIN ANALYZE
SELECT
    po.num,
    po.o_date,
    p.first_name,
    p.last_name,
    p.email
FROM person_order po
JOIN person p ON p.id = po.person_id
WHERE p.last_name LIKE 'S%'
ORDER BY po.o_date DESC
LIMIT 100;

-- -------------------------------------------------------------
-- 3. Query on the largest associative table
-- -------------------------------------------------------------
EXPLAIN ANALYZE
SELECT
    h.ordernum,
    h.dishname,
    d.price,
    po.o_date
FROM hasordercook h
JOIN dish d ON d.name = h.dishname
JOIN person_order po ON po.num = h.ordernum
WHERE d.price > 15
ORDER BY po.o_date DESC
LIMIT 200;

-- -------------------------------------------------------------
-- 4. Complex join-heavy analysis query
-- -------------------------------------------------------------
EXPLAIN ANALYZE
SELECT
    p.id AS customer_id,
    p.first_name,
    p.last_name,
    COUNT(po.num) AS order_count,
    SUM(d.price) AS total_order_value
FROM person p
JOIN customer c ON c.personid = p.id
JOIN person_order po ON po.person_id = p.id
JOIN hasordercook hoc ON hoc.ordernum = po.num
JOIN dish d ON d.name = hoc.dishname
WHERE p.last_name LIKE 'M%'
GROUP BY p.id, p.first_name, p.last_name
HAVING COUNT(po.num) > 2
ORDER BY total_order_value DESC
LIMIT 100;

-- -------------------------------------------------------------
-- 5. Show the impact of missing index on a common filter
-- -------------------------------------------------------------
-- Before creating an index, the planner likely performs a full scan
-- or a large hash/join-backed operation on person_order.
EXPLAIN ANALYZE
SELECT *
FROM person_order
WHERE person_id = 42;

-- -------------------------------------------------------------
-- 6. Add a targeted B-Tree index to optimize lookups by customer
-- -------------------------------------------------------------
CREATE INDEX idx_person_order_person_id
    ON person_order (person_id);

-- -------------------------------------------------------------
-- 7. Re-run the same query to show the execution plan after index
-- -------------------------------------------------------------
EXPLAIN ANALYZE
SELECT *
FROM person_order
WHERE person_id = 42;

-- -------------------------------------------------------------
-- 8. Add a second index for lookup speed on order-to-dish relationship
-- -------------------------------------------------------------
CREATE INDEX idx_hasordercook_ordernum
    ON hasordercook (ordernum);

EXPLAIN ANALYZE
SELECT
    hoc.ordernum,
    hoc.dishname,
    d.price
FROM hasordercook hoc
JOIN dish d ON d.name = hoc.dishname
WHERE hoc.ordernum BETWEEN 1000 AND 1200
ORDER BY hoc.ordernum;

-- -------------------------------------------------------------
-- 9. Additional index on order date for reporting queries
-- -------------------------------------------------------------
CREATE INDEX idx_person_order_date
    ON person_order (o_date);

EXPLAIN ANALYZE
SELECT
    o_date,
    COUNT(*) AS total_orders
FROM person_order
WHERE o_date >= '2024-01-01'
GROUP BY o_date
ORDER BY o_date;

-- -------------------------------------------------------------
-- 10. Optional index on person last_name for customer lookups
-- -------------------------------------------------------------
CREATE INDEX idx_person_last_name
    ON person (last_name);

EXPLAIN ANALYZE
SELECT
    id,
    first_name,
    last_name,
    email
FROM person
WHERE last_name LIKE 'S%'
ORDER BY last_name, first_name
LIMIT 100;

-- =============================================================
-- Summary of performance gains
-- =============================================================
-- The queries above illustrate how Postgres chooses scan strategies
-- based on table size and available indexes.
--
-- Before indexing, large filtered joins often result in sequential
-- scans or expensive hash joins. After adding a targeted B-Tree index,
-- the planner can use Index Scan / Bitmap Index Scan and dramatically
-- reduce execution time for lookup-heavy queries.
--
-- In portfolio work, this is a strong demonstration of:
--   - query tuning awareness
--   - understanding of execution plans
--   - ability to reason about large-table access patterns
--   - targeted index design for real-world OLTP workloads
--
-- Expected improvements:
--   - faster customer-order lookups
--   - reduced full scans on person_order
--   - improved join performance on order and order-item tables
--   - more efficient reporting on date and customer history queries
-- =============================================================
