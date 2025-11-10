---
name: dev-query-optimization
description: Use when working with database query optimization - provides comprehensive best practices for SQL, NoSQL, and ORM performance tuning
---

# Query Optimization

## When to Use
Use this skill when:
- Queries are slow (>100ms for simple queries, >1s for complex)
- Database CPU/memory usage is high
- Application experiences performance bottlenecks
- Implementing new database features
- Dealing with N+1 query problems in ORMs
- Optimizing pagination for large datasets
- Scaling applications to handle more traffic

## Process Overview
1. **Measure** - Profile queries, identify slow operations, establish baseline metrics
2. **Analyze** - Use EXPLAIN plans, identify missing indexes, spot anti-patterns
3. **Optimize** - Apply index strategies, rewrite queries, fix ORM issues
4. **Validate** - Re-measure performance, verify improvements, monitor production
5. **Monitor** - Track query performance over time, watch for regressions

---

## Index Strategies

### Index Types and Use Cases

#### B-Tree Indexes (Default)
Best for: Equality and range queries, sorting operations
```sql
-- PostgreSQL/MySQL default index
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_orders_created ON orders(created_at);

-- Good for queries like:
SELECT * FROM users WHERE email = 'user@example.com';
SELECT * FROM orders WHERE created_at > '2024-01-01' ORDER BY created_at;
```

#### Hash Indexes (PostgreSQL)
Best for: Exact equality comparisons only
```sql
-- PostgreSQL only - faster for equality, no range support
CREATE INDEX idx_users_username_hash ON users USING HASH (username);

-- Good for:
SELECT * FROM users WHERE username = 'johndoe';

-- NOT good for:
SELECT * FROM users WHERE username LIKE 'john%';  -- Won't use hash index
```

#### Composite (Multi-Column) Indexes
Best for: Queries filtering on multiple columns
```sql
-- Order matters! Most selective column first (ESR rule: Equality, Sort, Range)
CREATE INDEX idx_orders_user_status_created
ON orders(user_id, status, created_at);

-- Supports these queries efficiently:
SELECT * FROM orders WHERE user_id = 123;  -- Uses index
SELECT * FROM orders WHERE user_id = 123 AND status = 'pending';  -- Uses index
SELECT * FROM orders WHERE user_id = 123 AND status = 'pending'
ORDER BY created_at;  -- Fully uses index

-- Does NOT support:
SELECT * FROM orders WHERE status = 'pending';  -- Doesn't use index (skips first column)
```

**ESR Rule**: Design composite indexes as **Equality, Sort, Range**
- Equality conditions first (WHERE col = value)
- Sort columns next (ORDER BY col)
- Range conditions last (WHERE col > value)

#### Covering Indexes
Best for: Queries that can be satisfied entirely from index (no table lookup)
```sql
-- Include all queried columns in index
CREATE INDEX idx_users_email_name_covering
ON users(email) INCLUDE (first_name, last_name);

-- This query only reads the index (no table scan):
SELECT first_name, last_name FROM users WHERE email = 'user@example.com';
```

#### Partial Indexes
Best for: Indexing subset of rows that match specific criteria
```sql
-- Index only active users
CREATE INDEX idx_active_users_email
ON users(email) WHERE status = 'active';

-- Saves space, faster updates, optimized for common queries:
SELECT * FROM users WHERE email = 'user@example.com' AND status = 'active';
```

#### Full-Text Indexes (PostgreSQL GIN)
Best for: Text search with natural language queries
```sql
-- PostgreSQL full-text search
CREATE INDEX idx_posts_content_fts
ON posts USING GIN (to_tsvector('english', content));

-- Search query:
SELECT * FROM posts
WHERE to_tsvector('english', content) @@ to_tsquery('english', 'database & optimization');
```

### When to Create Indexes

**Always index:**
- Primary keys (automatic)
- Foreign keys (manual in most databases)
- Columns in WHERE clauses of frequent queries
- Columns in JOIN conditions
- Columns in ORDER BY clauses

**Consider indexing:**
- Columns in GROUP BY clauses
- Columns with high cardinality (many unique values)
- Columns frequently used for sorting

**Avoid indexing:**
- Small tables (<1000 rows) - sequential scan is faster
- Low cardinality columns (status with 2-3 values) - unless using partial indexes
- Columns with frequent writes and rare reads
- Tables with too many indexes (>5-7) - slows INSERT/UPDATE/DELETE

### Index Performance Impact

**Before optimization (no index):**
```sql
EXPLAIN ANALYZE SELECT * FROM orders WHERE user_id = 12345;

Seq Scan on orders  (cost=0.00..18456.00 rows=1234 width=120)
                    (actual time=2153.456..2153.789 rows=1234 loops=1)
  Filter: (user_id = 12345)
  Rows Removed by Filter: 998766
Planning Time: 0.123 ms
Execution Time: 2153.912 ms  ⚠️ 2.1 seconds!
```

**After indexing:**
```sql
CREATE INDEX idx_orders_user_id ON orders(user_id);

EXPLAIN ANALYZE SELECT * FROM orders WHERE user_id = 12345;

Index Scan using idx_orders_user_id on orders
  (cost=0.42..45.67 rows=1234 width=120)
  (actual time=0.123..1.456 rows=1234 loops=1)
  Index Cond: (user_id = 12345)
Planning Time: 0.089 ms
Execution Time: 1.678 ms  ✓ 1.7ms (99.9% improvement!)
```

---

## Query Analysis with EXPLAIN

### EXPLAIN vs EXPLAIN ANALYZE

**EXPLAIN** - Shows estimated execution plan (doesn't run query):
```sql
EXPLAIN SELECT * FROM users WHERE email = 'test@example.com';
```

**EXPLAIN ANALYZE** - Runs query and shows actual performance:
```sql
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'test@example.com';
```

**⚠️ Warning**: EXPLAIN ANALYZE executes the query, including INSERT/UPDATE/DELETE. Wrap destructive operations in a transaction:
```sql
BEGIN;
EXPLAIN ANALYZE DELETE FROM users WHERE status = 'inactive';
ROLLBACK;  -- Don't actually delete!
```

### Reading EXPLAIN Output

Key metrics to look for:

**1. Cost**: Estimated resource usage (arbitrary units)
```
cost=0.00..18456.00
```
- First number: startup cost
- Second number: total cost
- Lower is better

**2. Rows**: Estimated vs actual row counts
```
rows=1234  -- Estimated
(actual ... rows=5678 loops=1)  -- Actual
```
- Large discrepancy = outdated statistics → Run `ANALYZE table_name;`

**3. Time**: Actual execution time in milliseconds
```
(actual time=0.123..1.456 rows=1234 loops=1)
```
- First number: time to first row
- Second number: total time
- Focus optimization on nodes with highest time

**4. Scan Types** (from best to worst):
- **Index Scan** / **Index Only Scan** ✓ Fast, uses index
- **Bitmap Index Scan** ✓ Good for multiple conditions
- **Seq Scan** ⚠️ Full table scan - consider adding index
- **Seq Scan with Filter** 🚨 Scanning and discarding rows - needs index

### EXPLAIN Best Practices

**PostgreSQL** - Use BUFFERS to see I/O:
```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM orders WHERE user_id = 123;

-- Output shows disk reads:
-- Buffers: shared hit=8 read=1024
-- (8 pages from cache, 1024 from disk)
```

**MySQL** - Use EXPLAIN with FORMAT=JSON for details:
```sql
EXPLAIN FORMAT=JSON
SELECT * FROM orders WHERE user_id = 123\G
```

**Visualization tools**:
- PostgreSQL: https://explain.dalibo.com/ or https://explain.depesz.com/
- MySQL: Use MySQL Workbench Visual Explain

### Common EXPLAIN Red Flags

1. **"Seq Scan" on large tables** → Add index
2. **"rows=100 actual rows=10000"** → Run ANALYZE to update statistics
3. **High "loops" value** → Nested loop inefficiency, consider JOIN order
4. **"Filter: (condition)"** → Index isn't being used, check WHERE clause
5. **"Rows Removed by Filter"** → Many rows scanned and discarded, need better index

---

## Common Anti-Patterns

### 1. N+1 Query Problem

**Problem**: One query to get parent records, then N queries for each child

**Bad (N+1 queries):**
```python
# SQLAlchemy - lazy loading causes N+1
users = session.query(User).all()  # 1 query
for user in users:
    print(user.posts)  # N queries (one per user)!

# Generates:
# SELECT * FROM users;  -- 1 query
# SELECT * FROM posts WHERE user_id = 1;  -- query 1
# SELECT * FROM posts WHERE user_id = 2;  -- query 2
# ... (100 more queries for 100 users!)
```

**Good (2 queries with eager loading):**
```python
# SQLAlchemy - eager loading
users = session.query(User).options(joinedload(User.posts)).all()

# Generates:
# SELECT users.*, posts.* FROM users
# LEFT JOIN posts ON users.id = posts.user_id;  -- 1 query!
```

**Sequelize (Node.js) example:**
```javascript
// Bad - N+1
const users = await User.findAll();
for (const user of users) {
  const posts = await user.getPosts();  // N queries
}

// Good - eager loading
const users = await User.findAll({
  include: [{ model: Post }]  // 1 query with JOIN
});
```

**Prisma example:**
```typescript
// Bad - N+1 (though Prisma batches these)
const users = await prisma.user.findMany();
for (const user of users) {
  const posts = await prisma.post.findMany({
    where: { userId: user.id }  // Still inefficient
  });
}

// Good - nested read
const users = await prisma.user.findMany({
  include: { posts: true }  // Efficient nested query
});
```

### 2. SELECT * Anti-Pattern

**Bad**:
```sql
-- Fetches all 50 columns, even if you only need 3
SELECT * FROM users WHERE id = 123;
```

**Good**:
```sql
-- Only fetch what you need
SELECT id, email, first_name FROM users WHERE id = 123;
```

**Impact**:
- Network transfer: 5KB → 0.5KB (10x reduction)
- Prevents covering index usage
- Breaks queries when columns are added/removed

### 3. Missing WHERE Clause Indexes

**Bad**:
```sql
-- No index on status column
SELECT * FROM orders WHERE status = 'pending';
-- Result: Full table scan (2.5s for 1M rows)
```

**Good**:
```sql
CREATE INDEX idx_orders_status ON orders(status);
SELECT * FROM orders WHERE status = 'pending';
-- Result: Index scan (15ms)
```

### 4. Function Calls in WHERE Clause

**Bad (prevents index usage)**:
```sql
-- Function on indexed column prevents index usage
SELECT * FROM users WHERE LOWER(email) = 'user@example.com';
SELECT * FROM orders WHERE DATE(created_at) = '2024-01-15';
```

**Good**:
```sql
-- Use expression index or restructure query
CREATE INDEX idx_users_email_lower ON users(LOWER(email));
SELECT * FROM users WHERE LOWER(email) = 'user@example.com';

-- Or better: normalize data on insert
SELECT * FROM users WHERE email = 'user@example.com';  -- Uses regular index

-- For dates, use range:
SELECT * FROM orders
WHERE created_at >= '2024-01-15'
  AND created_at < '2024-01-16';
```

### 5. OR vs IN

**Bad (slow with multiple ORs)**:
```sql
SELECT * FROM products
WHERE category_id = 1 OR category_id = 5 OR category_id = 8;
```

**Good (faster with IN)**:
```sql
SELECT * FROM products
WHERE category_id IN (1, 5, 8);
-- Can use bitmap index scan for efficiency
```

**Even better (for large IN lists)**:
```sql
-- Use temporary table or VALUES list for 100+ items
SELECT p.* FROM products p
JOIN (VALUES (1), (5), (8)) AS cats(id)
ON p.category_id = cats.id;
```

### 6. Implicit Type Conversions

**Bad**:
```sql
-- user_id is INTEGER, but passed as string
SELECT * FROM orders WHERE user_id = '12345';  -- Prevents index usage!
```

**Good**:
```sql
SELECT * FROM orders WHERE user_id = 12345;  -- Uses index
```

---

## JOIN Optimization

### JOIN Types and Performance

**INNER JOIN** (fastest) - Only matching rows:
```sql
SELECT o.id, u.name
FROM orders o
INNER JOIN users u ON o.user_id = u.id
WHERE o.status = 'pending';
```

**LEFT JOIN** - All left table rows + matching right:
```sql
SELECT u.name, COUNT(o.id) AS order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id, u.name;
```

**RIGHT JOIN** (rare) - All right table rows + matching left
**FULL OUTER JOIN** (slowest) - All rows from both tables

### JOIN Order Matters

**Bad (large table first)**:
```sql
-- Starts with 1M rows, then filters
SELECT * FROM orders o
JOIN users u ON o.user_id = u.id
WHERE u.status = 'active';
-- Result: Scans 1M orders first
```

**Good (filter first)**:
```sql
-- Starts with 10K active users, then joins
SELECT * FROM users u
JOIN orders o ON u.id = o.user_id
WHERE u.status = 'active';
-- Result: Only processes 10K users' orders
```

**Best (use CTEs or subqueries to pre-filter)**:
```sql
WITH active_users AS (
  SELECT id FROM users WHERE status = 'active'
)
SELECT o.* FROM orders o
JOIN active_users u ON o.user_id = u.id;
```

### JOIN Index Requirements

**Both JOIN columns must be indexed:**
```sql
-- Index both sides of JOIN condition
CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_users_id ON users(id);  -- Usually automatic via PRIMARY KEY

SELECT * FROM orders o
JOIN users u ON o.user_id = u.id;  -- Now efficient
```

---

## Pagination Optimization

### OFFSET Pagination (Simple but Slow)

**Implementation**:
```sql
-- Page 1
SELECT * FROM posts ORDER BY created_at DESC LIMIT 20 OFFSET 0;

-- Page 100 (must scan first 2000 rows!)
SELECT * FROM posts ORDER BY created_at DESC LIMIT 20 OFFSET 2000;
```

**Performance degradation**:
```
Page 1:   OFFSET 0     → 5ms
Page 10:  OFFSET 200   → 15ms
Page 100: OFFSET 2000  → 150ms
Page 500: OFFSET 10000 → 2.5s  ⚠️ 500x slower!
```

**Problems**:
- Scans and discards all OFFSET rows (wasted work)
- Performance degrades linearly with page depth
- Results inconsistent if data changes between requests
- Not suitable for deep pagination or infinite scroll

### Cursor-Based Pagination (Fast and Scalable)

**Keyset pagination** using indexed column:

```sql
-- Page 1: Get first 20 posts
SELECT * FROM posts
ORDER BY created_at DESC, id DESC
LIMIT 20;

-- Returns: last row has created_at='2024-01-15 10:00:00', id=12345

-- Page 2: Use last row as cursor
SELECT * FROM posts
WHERE (created_at, id) < ('2024-01-15 10:00:00', 12345)
ORDER BY created_at DESC, id DESC
LIMIT 20;
```

**Performance - constant time**:
```
Page 1:   5ms
Page 10:  5ms  ✓
Page 100: 5ms  ✓
Page 500: 5ms  ✓ 500x faster than OFFSET!
```

**ORM Implementation (Prisma)**:
```typescript
// First page
const firstPage = await prisma.post.findMany({
  take: 20,
  orderBy: { createdAt: 'desc' }
});

// Next page using cursor
const nextPage = await prisma.post.findMany({
  take: 20,
  skip: 1,  // Skip the cursor itself
  cursor: { id: lastPost.id },
  orderBy: { createdAt: 'desc' }
});
```

**API Response Format**:
```json
{
  "data": [...],
  "pagination": {
    "next_cursor": "eyJpZCI6MTIzNDUsImNyZWF0ZWRBdCI6IjIwMjQtMDEtMTUifQ==",
    "has_more": true
  }
}
```

**Trade-offs**:
- ✓ Constant performance regardless of page depth
- ✓ Consistent results even with data changes
- ✓ Perfect for infinite scroll
- ✗ Can't jump to arbitrary page numbers
- ✗ Requires indexed column for cursor

---

## Aggregation Optimization

### GROUP BY Optimization

**Ensure GROUP BY columns are indexed**:
```sql
-- Without index: full table scan + sort
SELECT category, COUNT(*)
FROM products
GROUP BY category;
-- Time: 1.2s

-- With index: uses index for grouping
CREATE INDEX idx_products_category ON products(category);
-- Time: 45ms (26x faster)
```

**Avoid functions in GROUP BY**:
```sql
-- Bad (can't use index)
SELECT DATE(created_at), COUNT(*)
FROM orders
GROUP BY DATE(created_at);

-- Good (uses index)
SELECT created_at::date, COUNT(*)
FROM orders
GROUP BY created_at::date;

-- Best (pre-computed column)
ALTER TABLE orders ADD COLUMN created_date DATE;
CREATE INDEX idx_orders_created_date ON orders(created_date);
SELECT created_date, COUNT(*) FROM orders GROUP BY created_date;
```

### Materialized Views (Pre-computed Aggregations)

**For expensive recurring aggregations**:
```sql
-- Create materialized view
CREATE MATERIALIZED VIEW daily_sales_summary AS
SELECT
  DATE(created_at) AS sale_date,
  COUNT(*) AS order_count,
  SUM(total) AS total_revenue
FROM orders
GROUP BY DATE(created_at);

CREATE INDEX idx_daily_sales_date ON daily_sales_summary(sale_date);

-- Query is instant (data pre-computed)
SELECT * FROM daily_sales_summary
WHERE sale_date >= '2024-01-01';
-- Time: 2ms (was 5s on raw table)

-- Refresh periodically (e.g., nightly cron job)
REFRESH MATERIALIZED VIEW daily_sales_summary;
```

### Summary Tables

**For dashboard metrics**:
```sql
-- Summary table updated via trigger or cron
CREATE TABLE user_stats (
  user_id INT PRIMARY KEY,
  total_orders INT,
  total_spent DECIMAL(10,2),
  last_order_date DATE,
  updated_at TIMESTAMP
);

-- Update incrementally
CREATE OR REPLACE FUNCTION update_user_stats()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO user_stats (user_id, total_orders, total_spent, last_order_date)
  VALUES (NEW.user_id, 1, NEW.total, NEW.created_at)
  ON CONFLICT (user_id) DO UPDATE
  SET total_orders = user_stats.total_orders + 1,
      total_spent = user_stats.total_spent + NEW.total,
      last_order_date = GREATEST(user_stats.last_order_date, NEW.created_at),
      updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Fast queries
SELECT * FROM user_stats WHERE total_orders > 10;
-- Time: 5ms (was 2s aggregating from orders table)
```

---

## Full-Text Search

### PostgreSQL Full-Text Search

**Setup**:
```sql
-- Add tsvector column for full-text index
ALTER TABLE articles ADD COLUMN content_tsv tsvector;

-- Populate tsvector column
UPDATE articles
SET content_tsv = to_tsvector('english', title || ' ' || body);

-- Create GIN index
CREATE INDEX idx_articles_content_tsv ON articles USING GIN(content_tsv);

-- Keep updated via trigger
CREATE TRIGGER articles_content_tsv_update
BEFORE INSERT OR UPDATE ON articles
FOR EACH ROW EXECUTE FUNCTION
  tsvector_update_trigger(content_tsv, 'pg_catalog.english', title, body);
```

**Query**:
```sql
-- Simple search
SELECT * FROM articles
WHERE content_tsv @@ to_tsquery('english', 'database & optimization');

-- Ranked results
SELECT *, ts_rank(content_tsv, query) AS rank
FROM articles, to_tsquery('english', 'database & optimization') query
WHERE content_tsv @@ query
ORDER BY rank DESC;
```

**Performance**:
- Full table scan with LIKE: 5s
- Full-text search with GIN index: 25ms

### When to Use Elasticsearch

**Use PostgreSQL FTS when**:
- Simple text search needs
- <1M documents
- Already using PostgreSQL
- Want to keep data in one place

**Use Elasticsearch when**:
- Complex relevance ranking needed
- Faceted search, aggregations
- >10M documents
- Need sub-50ms search times
- Multi-language search with advanced stemming

---

## NoSQL Optimization

### MongoDB Query Optimization

**Index strategies**:
```javascript
// Create compound index (ESR rule applies)
db.orders.createIndex({ userId: 1, status: 1, createdAt: -1 });

// Covered query (all fields in index)
db.orders.createIndex({ userId: 1, total: 1 });
db.orders.find({ userId: 12345 }, { _id: 0, userId: 1, total: 1 });
// Returns: "executionStats" -> "totalDocsExamined": 0 (index-only!)

// Partial index (index subset)
db.orders.createIndex(
  { userId: 1, createdAt: 1 },
  { partialFilterExpression: { status: 'active' } }
);
```

**Analyze queries**:
```javascript
// Use explain() to see execution plan
db.orders.find({ userId: 12345 }).explain('executionStats');

// Look for:
// - "stage": "COLLSCAN" → Bad (collection scan)
// - "stage": "IXSCAN" → Good (index scan)
// - "totalDocsExamined" vs "nReturned" → Should be close
```

**Projection (select specific fields)**:
```javascript
// Bad - returns entire document
db.users.find({ email: 'user@example.com' });

// Good - only return needed fields
db.users.find(
  { email: 'user@example.com' },
  { email: 1, name: 1, _id: 0 }
);
```

### DynamoDB Key Design

**Partition key selection** (critical for performance):
```
Good partition keys (high cardinality):
- userId (millions of unique values)
- orderId (unique per order)
- email (unique per user)

Bad partition keys (low cardinality):
- status (few values like 'active'/'inactive')
- country (limited number of countries)
- createdDate (only 365 values per year)
```

**Composite primary key**:
```javascript
// Partition key + Sort key for flexible queries
const params = {
  TableName: 'Orders',
  KeySchema: [
    { AttributeName: 'userId', KeyType: 'HASH' },  // Partition key
    { AttributeName: 'createdAt', KeyType: 'RANGE' }  // Sort key
  ]
};

// Efficient queries
dynamodb.query({
  TableName: 'Orders',
  KeyConditionExpression: 'userId = :uid AND createdAt > :date',
  ExpressionAttributeValues: {
    ':uid': '12345',
    ':date': '2024-01-01'
  }
});
```

**Global Secondary Index (GSI)** for alternate access patterns:
```javascript
// GSI for querying by email
const gsiParams = {
  GlobalSecondaryIndexes: [{
    IndexName: 'email-index',
    KeySchema: [
      { AttributeName: 'email', KeyType: 'HASH' }
    ],
    Projection: { ProjectionType: 'ALL' }
  }]
};

// ⚠️ GSIs cost money - only create what you need
// Each GSI increases write costs
```

**Avoid Scan operations**:
```javascript
// Bad - scans entire table
dynamodb.scan({ TableName: 'Orders' });

// Good - use Query with key
dynamodb.query({
  TableName: 'Orders',
  KeyConditionExpression: 'userId = :uid'
});
```

### Redis Data Structure Optimization

**Choose right data structure**:
```javascript
// String: Simple key-value
await redis.set('user:12345', JSON.stringify(userData));

// Hash: Object with fields (more memory efficient)
await redis.hset('user:12345', {
  name: 'John',
  email: 'john@example.com'
});

// Sorted Set: Leaderboards, rankings
await redis.zadd('leaderboard', 1000, 'player1');
await redis.zadd('leaderboard', 950, 'player2');
await redis.zrevrange('leaderboard', 0, 9);  // Top 10

// List: Queues, activity feeds
await redis.lpush('notifications:user:12345', notification);
```

**Indexing with RediSearch**:
```javascript
// Create search index
await redis.call('FT.CREATE', 'productIdx',
  'ON', 'HASH', 'PREFIX', '1', 'product:',
  'SCHEMA', 'name', 'TEXT', 'price', 'NUMERIC'
);

// Search query
const results = await redis.call('FT.SEARCH', 'productIdx',
  '@name:laptop @price:[500 1000]'
);
```

---

## ORM Pitfalls and Solutions

### 1. Lazy Loading (N+1 Problem)

See "N+1 Query Problem" section above for detailed examples.

**Quick fix checklist**:
- SQLAlchemy: Use `joinedload()`, `selectinload()`, or `subqueryload()`
- Sequelize: Use `include` option
- Prisma: Use `include` in queries
- ActiveRecord: Use `.includes()` or `.eager_load()`

### 2. Missing Eager Loading

**Bad**:
```python
# SQLAlchemy - multiple separate queries
users = session.query(User).all()
posts = session.query(Post).filter(Post.user_id.in_([u.id for u in users])).all()
```

**Good**:
```python
# Single query with JOIN
users = session.query(User).options(joinedload(User.posts)).all()
```

### 3. Over-fetching Data

**Bad**:
```python
# Loads all columns for all users
users = session.query(User).all()
for user in users:
    print(user.email)  # Only need email!
```

**Good**:
```python
# Only load needed columns
emails = session.query(User.email).all()
```

### 4. When to Use Raw SQL

**Use ORM when**:
- CRUD operations
- Simple queries
- Relationships are straightforward
- Type safety matters

**Use raw SQL when**:
- Complex aggregations
- Window functions
- Database-specific features (JSONB operators, full-text search)
- Performance-critical queries
- Bulk operations

```python
# SQLAlchemy raw SQL
result = session.execute(text("""
  SELECT date_trunc('day', created_at) AS day,
         COUNT(*) AS count
  FROM orders
  WHERE created_at > :start_date
  GROUP BY day
  ORDER BY day DESC
"""), {"start_date": start_date})
```

---

## Monitoring and Tools

### PostgreSQL Tools

**pg_stat_statements** - Track query performance:
```sql
-- Enable extension
CREATE EXTENSION pg_stat_statements;

-- Find slowest queries
SELECT
  query,
  calls,
  total_exec_time / 1000 AS total_time_seconds,
  mean_exec_time AS avg_time_ms
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 10;

-- Find queries with high variance
SELECT query, mean_exec_time, stddev_exec_time
FROM pg_stat_statements
WHERE stddev_exec_time > mean_exec_time * 0.5
ORDER BY stddev_exec_time DESC;
```

**Auto-explain** - Log slow query plans:
```sql
-- In postgresql.conf
shared_preload_libraries = 'auto_explain'
auto_explain.log_min_duration = 1000  -- Log queries > 1s
auto_explain.log_analyze = on
```

**Index usage statistics**:
```sql
-- Find unused indexes
SELECT schemaname, tablename, indexname, idx_scan
FROM pg_stat_user_indexes
WHERE idx_scan = 0
  AND indexname NOT LIKE '%_pkey'
ORDER BY pg_relation_size(indexrelid) DESC;
```

### MySQL Tools

**Slow Query Log**:
```sql
-- Enable slow query log
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 1;  -- Log queries > 1s

-- Analyze with pt-query-digest (Percona Toolkit)
pt-query-digest /var/log/mysql/slow-query.log
```

**Performance Schema**:
```sql
-- Find slowest queries
SELECT query, count_star, avg_timer_wait / 1000000000000 AS avg_seconds
FROM performance_schema.events_statements_summary_by_digest
ORDER BY avg_timer_wait DESC
LIMIT 10;
```

### Application Monitoring

**Tools**:
- New Relic: Transaction tracing, slow query detection
- Datadog: APM with database performance monitoring
- pganalyze (PostgreSQL): Query analysis and indexing recommendations
- MongoDB Atlas: Built-in performance advisor

---

## Success Criteria

**Performance targets**:
- Simple queries (single table, indexed): <10ms
- Complex queries (multiple JOINs): <100ms
- Aggregations: <500ms
- Full-text search: <50ms

**Optimization goals**:
- 80% of queries use indexes (check with EXPLAIN)
- Zero N+1 queries in production code
- <5% slow query log entries
- Query time P95 <500ms, P99 <2s

**Monitoring checklist**:
- [ ] Slow query logging enabled
- [ ] pg_stat_statements or equivalent tracking queries
- [ ] Unused indexes identified and removed
- [ ] Query performance regression alerts set up
- [ ] Database connection pool properly sized

---

## Related Skills
- `indexing-strategies` - Deep dive into index types and design
- `database-design` - Schema design for optimal query performance
- `connection-pooling` - Connection management for high-traffic apps
- `caching-strategies` - Redis/Memcached for query result caching
- `api-design` - Designing APIs with query performance in mind

---

## References

### Documentation
- PostgreSQL EXPLAIN: https://www.postgresql.org/docs/current/using-explain.html
- MySQL EXPLAIN: https://dev.mysql.com/doc/refman/8.0/en/explain.html
- MongoDB Index Strategies: https://www.mongodb.com/docs/manual/applications/indexes/
- DynamoDB Best Practices: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/best-practices.html

### Tools
- EXPLAIN Visualizers: https://explain.dalibo.com/ | https://explain.depesz.com/
- pganalyze: https://pganalyze.com/
- Percona Toolkit: https://www.percona.com/software/database-tools/percona-toolkit
- MongoDB Compass: https://www.mongodb.com/products/compass

### Learning Resources
- Use The Index, Luke: https://use-the-index-luke.com/
- PostgreSQL Performance Wiki: https://wiki.postgresql.org/wiki/Performance_Optimization
- SQL Indexing and Tuning e-Book: https://use-the-index-luke.com/sql/preface
