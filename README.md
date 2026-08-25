# Restaurant RDBMS Architecture

## Project Overview
This project defines a fully normalized relational database architecture for a restaurant business expanding from a single branch to a multi-branch operation and launching a customer ordering application. The design resolves prior data limitations by supporting branch-level operations, menu management (dishes, recipes, serving times), multiple user roles (customers, employees, and chefs with specialization and tutor hierarchy), and a transactional order workflow that connects branches, customers, and chefs.

## Database Design
The design process started with conceptual ER modeling to capture business entities, attributes, and relationship cardinalities, then translated that model into a relational schema with clear keys and constraints for implementation in SQL.

![Conceptual ER Diagram](er_diagram.png)

![Relational Schema](relational_schema.png)

## Technical Highlights
- Composite key design for relationship and transactional consistency.
- Cascading foreign key constraints to preserve referential integrity.
- Multi-table INNER and OUTER joins for reporting and operational analysis.
- Nested subqueries for advanced filtering, aggregation, and business logic extraction.

## Tech Stack
- SQL (Oracle/PostgreSQL compatible)
- Relational Database Management Systems (RDBMS)
- Entity-Relationship Modeling

## Files Included
- `schema_and_queries.sql`: DDL for 10 normalized tables and DML/SELECT statements covering complex analytical and transactional queries.
