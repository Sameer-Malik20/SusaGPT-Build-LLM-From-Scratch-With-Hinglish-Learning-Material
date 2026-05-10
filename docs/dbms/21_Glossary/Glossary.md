# 📖 Database Glossary: The A-Z of DBMS
> **Objective:** A comprehensive reference for all the technical terms and jargon used in the world of database engineering | **Language:** Hinglish | **Standard:** 2026 Expert Framework

---

## 🅰️ A
- **ACID:** Atomicity, Consistency, Isolation, Durability. The core properties of a reliable database.
- **Aggregate Function:** A function (SUM, AVG, MIN, MAX) that operates on a group of rows.
- **ALTO (Active-Low-Transactional-Operations):** A modern 2026 term for low-overhead transactions.
- **ANN (Approximate Nearest Neighbor):** Search algorithm used in Vector databases.

## 🅱️ B
- **B-Tree:** The most common data structure used for database indexing.
- **Binary Log (Binlog):** A record of all changes to the database data (MySQL).
- **Blob:** Binary Large Object (for storing images/files).
- **Buffer Pool:** A memory area where the DB caches data pages from disk.

## 🅲 C
- **CAP Theorem:** Consistency, Availability, Partition Tolerance (Choose 2).
- **CDC (Change Data Capture):** Streaming database changes to other systems in real-time.
- **Checkpoint:** The process of writing "Dirty" pages from RAM to the main disk file.
- **Clustered Index:** An index that defines the physical order of data on the disk.
- **CTE (Common Table Expression):** A temporary result set using the `WITH` clause.

## 🅳 D
- **DaaS (Database as a Service):** Managed cloud databases like AWS RDS.
- **Deadlock:** A situation where two transactions are waiting for each other to release locks.
- **Denormalization:** Intentionally adding redundancy to speed up reads.
- **Dirty Read:** Reading data that has been updated by another transaction but not yet committed.

## 🅴 E
- **Embedding:** A vector representation of text or image data used in AI.
- **ETL (Extract, Transform, Load):** Moving data between different systems.
- **EXPLAIN:** A command used to view the Query Execution Plan.

## 🅵 F
- **Fan-out:** The number of child nodes a parent node has in a B-Tree.
- **Foreign Key:** A column that establishes a relationship between two tables.
- **Full Table Scan:** Reading every single row in a table (usually slow).

## 🅶 G
- **Gossip Protocol:** How nodes in a distributed database share information about each other.
- **Graph Database:** A database that uses nodes and edges to store relationships.

## 🅷 H
- **Hash Join:** A fast way to join two large tables using a hash map in RAM.
- **HNSW (Hierarchical Navigable Small World):** A graph-based index for vectors.
- **Horizontal Scaling:** Adding more servers to a database cluster.

## 🅸 I
- **Idempotency:** An operation that can be performed multiple times without changing the result beyond the first application.
- **Index:** A data structure that makes data retrieval faster.
- **Isolation Level:** Defines how transaction integrity is visible to other users.

## 🅹 J
- **JSONB:** Binary JSON format used in Postgres for high-performance NoSQL-like storage.
- **Join:** Combining rows from two or more tables based on a related column.

## 🅻 L
- **LSM-Tree (Log-Structured Merge-Tree):** A data structure optimized for high write performance (Cassandra/RocksDB).
- **Latency:** The time it takes for a database to respond to a query.

## 🅼 M
- **Materialized View:** A view that physically stores the result of a query for faster access.
- **MVCC (Multi-Version Concurrency Control):** Allowing readers and writers to work simultaneously without locking.

## 🅾️ O
- **OLAP (Online Analytical Processing):** Optimized for complex data analysis and reports.
- **OLTP (Online Transaction Processing):** Optimized for fast, short transactions (Apps).
- **ORM (Object-Relational Mapping):** A library that lets you interact with a DB using code objects (e.g., Prisma, SQLAlchemy).

## 🅿️ P
- **Partitioning:** Splitting a large table into smaller, more manageable pieces.
- **Primary Key:** A unique identifier for every row in a table.

## 🆀 Q
- **Query Optimizer:** The "Brain" of the DB that decides the best way to execute a query.
- **Quorum:** The minimum number of nodes that must agree for a distributed operation to succeed.

## 🆁 R
- **R-Tree:** A spatial index used for mapping and geographic data.
- **RAG (Retrieval-Augmented Generation):** Connecting a database to an LLM for smart answers.
- **Read Replica:** A copy of the database used only for reading traffic.

## 🆂 S
- **Sharding:** Distributing data across multiple physical database servers.
- **Slow Query Log:** A log of all queries that took longer than a specific time.
- **SQL (Structured Query Language):** The standard language for relational databases.

## 🆃 T
- **Time-Series Database:** A database optimized for timestamped data (InfluxDB).
- **Transaction:** A sequence of operations performed as a single logical unit of work.

## 🆄 U
- **UPSERT:** An operation that either Inserts a new row or Updates an existing one.

## 🆅 V
- **Vector Database:** A database designed to store and search through embeddings (Pinecone/Weaviate).
- **Vertical Scaling:** Increasing the CPU or RAM of a single server.

## 🆆 W
- **WAL (Write-Ahead Logging):** Writing changes to a log file before applying them to the main data file.
- **Working Set:** The portion of your data that is frequently accessed and should fit in RAM.

漫
---

## 🏁 The End of the Journey
"Agar aapne ye saare terms samajh liye hain, toh aap Database Engineering ke maidan mein kisi se bhi ladd sakte hain. Happy Querying!"
漫
