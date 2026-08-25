# Restaurant PostgreSQL Architecture

## Project Architecture & Overview
This project models a multi-branch restaurant business as a normalized relational system designed for operational consistency, reporting, and scalable order processing. The database supports branch-level service delivery, dish and menu management, role-based customer and staff records, chef specialization, tutoring relationships, and high-volume order tracking.

The schema is designed around core restaurant operations and ensures referential integrity across linked entities. It captures the business logic needed to support:
- multiple restaurant branches
- menu offerings by branch
- customer orders and order-item relationships
- employee and chef role distinctions
- chef expertise and mentoring structure
- realistic SQL-based querying for analytics and operational review

This project evolved from a classroom relational design into a production-style portfolio system using PostgreSQL, Docker, and Python-driven data generation.

![Conceptual ER Diagram](er_diagram.png)

![Relational Schema](relational_schema.png)

## Tech Stack & Tools
- PostgreSQL 15
- Docker & Docker Compose
- Python 3
- Faker for synthetic data generation
- psycopg2-binary for Python-to-PostgreSQL connectivity
- SQL for schema creation, data loading, and execution-plan analysis
- `EXPLAIN ANALYZE` for performance tuning and query optimization

## System Highlights
- Normalized relational schema for a realistic restaurant domain
- Strong foreign key relationships and composite-key patterns
- Multi-table joins and reporting-oriented queries
- Large-scale synthetic dataset generation for portfolio demonstration
- Performance analysis using query execution plans and targeted B-Tree indexes
- Dockerized database deployment for local reproducibility

## Quick Start Guide

### 1) Start the database with Docker
From the project root, run:

```bash
docker compose up -d
```

This starts a PostgreSQL 15 instance using the configuration in `docker-compose.yml` and automatically initializes the schema from `init.sql`.

### 2) Install Python dependencies
```bash
python -m pip install -r requirements.txt
```

### 3) Generate mock data
Run the seeding script to populate the database with realistic records, including 5,000+ mock orders:

```bash
python seed_data.py
```

This script inserts:
- 3 restaurant branches
- 20 dishes
- 1,000 people across customers, employees, and chefs
- 5,000 orders
- relationally consistent order and chef/dish mappings

### 4) Run the performance tuning queries
Open PostgreSQL in your preferred client or use a SQL runner to execute:

```sql
\i performance_tuning.sql
```

This file contains the execution-plan analysis and index comparison examples.

## Performance Tuning & Observability Highlights
This project demonstrates a realistic database tuning workflow for a high-volume transactional system.

We used `EXPLAIN ANALYZE` to identify bottlenecks such as:
- large scans over `person_order`
- expensive join patterns between order records and customer/dish tables
- repeated lookups across large operational tables

After analyzing the plans, we applied targeted B-Tree indexes to optimize common access patterns, particularly around:
- customer-to-order lookups
- order-to-item relationship access
- reporting on order dates and customer history

This helps showcase the practical database engineering skill of translating execution-plan evidence into efficient indexing strategies for real workloads.

## File Structure
- `README.md` — project overview, architecture summary, setup guide, and performance notes
- `schema_and_queries.sql` — original SQL project source and learning-oriented relational schema
- `init.sql` — PostgreSQL-compatible schema used by the Docker container on startup
- `docker-compose.yml` — PostgreSQL 15 container configuration and initialization setup
- `requirements.txt` — Python dependencies for the seeding workflow
- `seed_data.py` — Python script that uses Faker and psycopg2 to generate realistic mock data
- `performance_tuning.sql` — query analysis, `EXPLAIN ANALYZE` examples, and index comparison work
- `er_diagram.png` — conceptual ER diagram of the business domain
- `relational_schema.png` — visualization of the relational model

## Portfolio Value
This repository demonstrates a strong combination of:
- database design
- SQL expertise
- PostgreSQL deployment via Docker
- Python-powered data seeding
- performance tuning and query optimization
- production-style project documentation

It is suitable as a DB portfolio project for showcasing real-world relational modeling and operational database skills.
