# E-Commerce PostgreSQL Database Project

A PostgreSQL-based **E-Commerce Database Management System** developed to demonstrate relational database design, SQL querying, query optimization, indexing, and backend integration using **FastAPI**.

This project covers database schema design, data generation, advanced SQL operations, performance optimization using **EXPLAIN ANALYZE**, and exposing the database through REST APIs.

---

# Features

- Relational database design using PostgreSQL
- Normalized database schema
- Python-based database seeding using Faker
- Advanced SQL JOIN queries
- Composite Indexes
- Query Optimization using EXPLAIN ANALYZE
- FastAPI backend connected to PostgreSQL
- REST APIs for Customers, Products, and Orders

---

# Tech Stack

### Database
- PostgreSQL
- SQL

### Backend
- Python
- FastAPI
- Psycopg2

### Libraries
- Faker
- python-dotenv
- Uvicorn

---

# Project Structure

```text
ecommerce-postgres/
│
├── README.md
├── requirements.txt
├── .env
├── .gitignore
│
├── database/
│   ├── connection.py
│   ├── seed.py
│   │
│   │
│   ├── queries/
│   │   ├── joins.sql
│   │   ├── create_tables.sql
│   │   ├── indexes.sql
│   │   └── optimization.sql
│      
│       
│
├── backend/
│   ├── app.py
│   ├── routes/
│   └── services/
│    
│
└── screenshots/
        └── er_diagram.md
```

---

# Database Schema

The project consists of six relational tables:

- Customers
- Categories
- Products
- Orders
- Order Items
- Payments

## Relationships

- One Customer → Many Orders
- One Category → Many Products
- One Order → Many Order Items
- One Product → Many Order Items
- One Order → One Payment

---

# Database Setup

## 1. Clone the Repository

```bash
git clone <https://github.com/tanyamishraTA/ecommerce-postgres>
cd ecommerce-postgres
```

---

## 2. Create Virtual Environment

```bash
python -m venv venv
```

### Activate the Virtual Environment

#### Windows

```bash
venv\Scripts\activate
```

#### macOS/Linux

```bash
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Create a `.env` file in the project root.

```env
DB_NAME=your_database_name
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

---

## 5. Create Database

```sql
CREATE DATABASE ecommerce_db;
```

---

## 6. Create Tables

Execute the SQL file:

```text
database/schema/create_tables.sql
```

using pgAdmin, psql, or any PostgreSQL client.

---

## 7. Seed the Database

```bash
python database/seed.py
```

This generates realistic data for:

- Categories
- Customers
- Products
- Orders
- Order Items
- Payments

---

# SQL Queries

The project includes SQL examples covering:

## JOIN Queries

- INNER JOIN
- LEFT JOIN
- RIGHT JOIN
- FULL OUTER JOIN
- Multiple INNER JOIN

Location:

```text
database/queries/joins.sql
```

---

## Composite Indexes

Two composite indexes were created to improve query performance.

### Orders Table

```sql
(customer_id, order_date)
```

### Products Table

```sql
(category_id, price)
```

Location:

```text
database/queries/indexes.sql
```

---

## Query Optimization

Performance comparison using:

```sql
EXPLAIN ANALYZE
```

demonstrating:

- Sequential Scan
- Bitmap Index Scan
- Bitmap Heap Scan

Location:

```text
database/queries/optimization.sql
```

---

# Backend API

The PostgreSQL database is connected to a FastAPI backend.

Run the server:

```bash
uvicorn backend.app:app --reload
```

Swagger Documentation:

```text
http://127.0.0.1:8000/docs
```

---

# API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | `/` | API health check |
| GET | `/customers` | Retrieve all customers |
| GET | `/products` | Retrieve all products |
| GET | `/orders` | Retrieve all orders |
| GET | `/customers/{customer_id}/orders` | Retrieve all orders for a specific customer |

---

# Performance Optimization

The project demonstrates PostgreSQL query optimization using composite indexes.

### Before Index

- Sequential Scan
- Entire table scanned

### After Index

- Bitmap Index Scan
- Bitmap Heap Scan
- Reduced execution time

Performance comparison is available in:

```text
database/queries/optimization.sql
```

---

# Learning Outcomes

This project demonstrates understanding of:

- PostgreSQL database design
- SQL constraints and relationships
- Primary Keys & Foreign Keys
- Database normalization
- Data seeding using Python
- Advanced JOIN operations
- Composite Indexes
- Query Optimization
- EXPLAIN ANALYZE
- FastAPI integration with PostgreSQL
- REST API development

---
