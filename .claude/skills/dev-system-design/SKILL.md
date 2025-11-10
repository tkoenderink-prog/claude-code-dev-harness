---
name: system-design
description: Use when designing scalable, reliable distributed systems - comprehensive guide covering architecture patterns, design principles, trade-offs, and real-world examples
---

# System Design

## When to Use

Invoke this skill when:
- Designing a new system or major feature from scratch
- Planning architecture for scalability (10K → 1M+ users)
- Making technology stack decisions for distributed systems
- Conducting system design interviews or reviews
- Evaluating trade-offs between consistency, availability, and partition tolerance
- Choosing between microservices, monolithic, serverless, or event-driven architectures
- Planning capacity, load balancing, caching, or database strategies
- Designing APIs, data models, or service boundaries
- Troubleshooting scalability bottlenecks in existing systems

## Core Design Principles

### 1. Scalability
**Definition**: System's ability to handle increased load by adding resources.

**Horizontal Scaling (Scale Out)**
- Add more machines/nodes to distribute load
- Better for stateless services (web servers, API gateways)
- Examples: Add more application servers behind load balancer
- Pros: No limit to scaling, fault tolerance
- Cons: Complexity in coordination, data consistency challenges

**Vertical Scaling (Scale Up)**
- Add more CPU, RAM, disk to existing machine
- Suitable for databases, stateful services
- Examples: Upgrade database server from 16GB → 128GB RAM
- Pros: Simple, no application changes
- Cons: Hardware limits, single point of failure, expensive

**Scaling Dimensions**
- **Data scaling**: Sharding, partitioning, replication
- **Traffic scaling**: Load balancing, CDN, caching
- **Geographic scaling**: Multi-region deployment, edge computing

### 2. Reliability
**Definition**: System continues to work correctly even when things go wrong.

**Fault Tolerance Strategies**
- **Redundancy**: Multiple instances, replica databases
- **Graceful degradation**: Reduce functionality instead of total failure
- **Circuit breakers**: Stop cascading failures
- **Health checks**: Detect and route around unhealthy nodes
- **Backups & disaster recovery**: Regular snapshots, multi-region replication

**Availability Targets**
- 99.9% (three nines) = 8.76 hours downtime/year
- 99.99% (four nines) = 52.56 minutes downtime/year
- 99.999% (five nines) = 5.26 minutes downtime/year

### 3. Maintainability
**Definition**: System is easy to understand, modify, and operate.

**Key Practices**
- **Modularity**: Clear service boundaries, loose coupling
- **Observability**: Comprehensive logging, metrics, tracing
- **Documentation**: Architecture diagrams, API docs, runbooks
- **Automation**: CI/CD, infrastructure as code, automated testing
- **Simplicity**: Avoid over-engineering, choose boring technology

### 4. Performance
**Definition**: System responds quickly under expected load.

**Performance Metrics**
- **Latency**: Time to process single request (P50, P95, P99)
- **Throughput**: Requests processed per second
- **Response time**: User-perceived time including network
- **Resource utilization**: CPU, memory, disk, network usage

**Optimization Strategies**
- **Caching**: Reduce database/computation load
- **Asynchronous processing**: Background jobs for non-critical tasks
- **Database indexing**: Speed up queries
- **Connection pooling**: Reuse database connections
- **Compression**: Reduce data transfer size

## Architecture Patterns

### Microservices vs Monolithic

**Monolithic Architecture**
```
┌─────────────────────────────┐
│     Monolithic App          │
│  ┌──────────────────────┐   │
│  │  User Service        │   │
│  │  Product Service     │   │
│  │  Order Service       │   │
│  │  Payment Service     │   │
│  └──────────────────────┘   │
│          ↓                  │
│  ┌──────────────────────┐   │
│  │  Single Database     │   │
│  └──────────────────────┘   │
└─────────────────────────────┘
```

**Pros**: Simple deployment, easier debugging, no network overhead
**Cons**: Tight coupling, difficult to scale, long CI/CD cycles
**Use when**: Small team, MVP, simple domain, low traffic (<10K daily users)

**Microservices Architecture**
```
┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐
│   User     │  │  Product   │  │   Order    │  │  Payment   │
│  Service   │  │  Service   │  │  Service   │  │  Service   │
└──────┬─────┘  └──────┬─────┘  └──────┬─────┘  └──────┬─────┘
       │               │               │               │
   ┌───▼───┐       ┌───▼───┐       ┌───▼───┐       ┌───▼───┐
   │User DB│       │Prod DB│       │Order  │       │Payment│
   └───────┘       └───────┘       │  DB   │       │  DB   │
                                   └───────┘       └───────┘
```

**Pros**: Independent deployment, technology flexibility, team autonomy, fine-grained scaling
**Cons**: Complex operations, distributed system challenges, network overhead
**Use when**: Large team, complex domain, need independent scaling, >100K users

### Event-Driven Architecture

**Pattern**: Services communicate via asynchronous events (pub/sub).

```
┌─────────┐      Event       ┌──────────────┐      ┌─────────┐
│ Order   │ ───publish────> │ Message      │ ───> │ Email   │
│ Service │                  │ Queue/Broker │      │ Service │
└─────────┘                  │ (Kafka/SQS)  │      └─────────┘
                             └──────────────┘
                                     │
                                     └──────────────> ┌──────────┐
                                                      │ Inventory│
                                                      │ Service  │
                                                      └──────────┘
```

**Pros**: Loose coupling, scalability, resilience, async processing
**Cons**: Eventual consistency, complex debugging, message ordering challenges
**Use when**: High throughput, background processing, multiple downstream consumers
**Examples**: Order processing, notification systems, analytics pipelines

### Serverless Architecture

**Pattern**: Event-triggered functions, fully managed infrastructure.

**Components**
- **Functions**: AWS Lambda, Azure Functions, Google Cloud Functions
- **API Gateway**: HTTP → Function routing
- **Storage**: S3, DynamoDB, Firestore
- **Events**: HTTP requests, file uploads, database changes, scheduled jobs

**Pros**: Auto-scaling, pay-per-use, no infrastructure management, fast iteration
**Cons**: Cold start latency, vendor lock-in, debugging complexity, stateless constraints
**Use when**: Unpredictable traffic, event processing, prototyping, cost optimization
**Examples**: Image processing, webhooks, scheduled reports, API backends

### CQRS (Command Query Responsibility Segregation)

**Pattern**: Separate read and write data models.

```
┌──────────┐     Commands      ┌──────────────┐
│  Client  │ ────(writes)────> │ Write Model  │
└──────────┘                    │ (normalized) │
     │                          └──────┬───────┘
     │                                 │
     │  Queries                   Events/Sync
     │  (reads)                        │
     │                          ┌──────▼───────┐
     └───────────────────────> │ Read Model   │
                                │ (denormalized│
                                │  for queries)│
                                └──────────────┘
```

**Pros**: Optimized reads and writes, scalability, complex query support
**Cons**: Eventual consistency, code duplication, operational complexity
**Use when**: Read/write patterns differ significantly, complex reporting needs
**Examples**: E-commerce (browsing vs purchasing), analytics dashboards

## System Components

### Load Balancers

**Purpose**: Distribute traffic across multiple servers.

**Algorithms**
- **Round Robin**: Cycle through servers equally
- **Least Connections**: Route to server with fewest active connections
- **IP Hash**: Same client → same server (sticky sessions)
- **Weighted**: Route based on server capacity

**Layers**
- **L4 (Transport)**: TCP/UDP level, faster, less flexible
- **L7 (Application)**: HTTP level, content-based routing, SSL termination

**Tools**: Nginx, HAProxy, AWS ALB/NLB, Google Cloud Load Balancer

### Caching Layers

**Cache Levels**
```
Browser Cache (client-side)
       ↓
CDN Cache (edge)
       ↓
Application Cache (server-side: Redis, Memcached)
       ↓
Database Query Cache
       ↓
Database (source of truth)
```

**Strategies**
- **Cache-Aside**: App checks cache → miss → load from DB → store in cache
- **Write-Through**: Write to cache and DB simultaneously
- **Write-Behind**: Write to cache → async write to DB
- **Refresh-Ahead**: Preemptively refresh cache before expiry

**Eviction Policies**
- **LRU** (Least Recently Used): Remove oldest accessed items
- **LFU** (Least Frequently Used): Remove least accessed items
- **TTL** (Time To Live): Expire after fixed time

**Use Cases**
- Session storage: Redis, Memcached
- API responses: Application-level cache
- Static assets: CDN (CloudFlare, CloudFront, Fastly)
- Database queries: Query result cache

### Databases

**Relational (SQL)**
- **Examples**: PostgreSQL, MySQL, MariaDB
- **Pros**: ACID guarantees, complex queries, mature tooling
- **Cons**: Harder to scale horizontally, schema rigidity
- **Use when**: Strong consistency, complex relationships, transactions

**NoSQL Types**

**Document Stores**
- **Examples**: MongoDB, CouchDB, Firestore
- **Use for**: Flexible schema, hierarchical data, rapid iteration
- **Example**: User profiles, product catalogs, content management

**Key-Value Stores**
- **Examples**: Redis, DynamoDB, Riak
- **Use for**: Simple lookups, caching, session storage
- **Example**: Session data, user preferences, feature flags

**Column-Family Stores**
- **Examples**: Cassandra, HBase, ScyllaDB
- **Use for**: Time-series data, high write throughput, wide tables
- **Example**: Analytics, IoT data, metrics storage

**Graph Databases**
- **Examples**: Neo4j, Amazon Neptune, ArangoDB
- **Use for**: Relationship-heavy data, social networks, recommendation engines
- **Example**: Social graphs, fraud detection, knowledge graphs

**Scaling Strategies**
- **Replication**: Master-slave (read scaling), multi-master (write scaling)
- **Sharding**: Partition data by key (user ID, geographic region)
- **Indexing**: Speed up queries, trade-off with write performance

### Message Queues

**Purpose**: Asynchronous communication, decoupling services.

**Patterns**
- **Queue**: Point-to-point, one consumer processes each message
- **Pub/Sub**: One-to-many, multiple subscribers receive same message
- **Topic**: Categorize messages by topic/channel

**Tools**
- **RabbitMQ**: Feature-rich, AMQP protocol, complex routing
- **Apache Kafka**: High throughput, log-based, event streaming
- **AWS SQS/SNS**: Managed, simple, serverless-friendly
- **Redis Pub/Sub**: Simple, in-memory, no persistence guarantees

**Use Cases**
- Background jobs (email sending, image processing)
- Order processing pipelines
- Event sourcing and CQRS
- Microservice communication

## Design Process

### 1. Requirements Gathering

**Functional Requirements**
- What features must the system support?
- What are the core user flows?
- What data needs to be stored and retrieved?

**Non-Functional Requirements**
- **Scale**: How many users? Requests per second? Data volume?
- **Performance**: Latency targets? Throughput goals?
- **Availability**: Uptime requirements? Geographic distribution?
- **Consistency**: Strong vs eventual consistency needs?

**Example: Design Instagram-like System**
- Users upload photos (10M users, 1M photos/day)
- View feed of followed users (100M reads/day)
- Like, comment on photos (50M writes/day)
- Average photo size: 2MB
- Low latency for feed (<200ms P95)

### 2. Capacity Planning

**Estimate Scale**
```
Daily Active Users (DAU): 10M
Photos uploaded/day: 1M
Average photo size: 2MB
Storage needed/day: 1M × 2MB = 2TB/day
Storage needed/year: 2TB × 365 = 730TB ≈ 1PB

Requests per second:
  Uploads: 1M / 86400s ≈ 12 QPS
  Reads: 100M / 86400s ≈ 1157 QPS
  Peak traffic (3x average): 3468 QPS

Bandwidth:
  Upload: 12 QPS × 2MB = 24 MB/s
  Download (assuming thumbnails 100KB): 1157 × 0.1MB = 116 MB/s
```

**Right-Size Resources**
- Application servers: 100 servers @ 50 QPS each = 5000 QPS capacity
- Database: Shard by user_id across 10 shards
- Cache: 20% hot data = 200GB Redis cluster
- Object storage: S3/GCS for photos

### 3. Component Design

**High-Level Architecture**
```
┌──────┐          ┌─────────────┐          ┌──────────┐
│Client│ ──────> │ Load        │ ──────> │ API      │
└──────┘          │ Balancer    │          │ Gateway  │
                  └─────────────┘          └────┬─────┘
                                                │
         ┌──────────────────────────────────────┼────────────────┐
         │                                      │                │
    ┌────▼─────┐                       ┌───────▼──────┐  ┌──────▼────┐
    │ Upload   │                       │ Feed Service │  │ User      │
    │ Service  │                       └───────┬──────┘  │ Service   │
    └────┬─────┘                               │         └──────┬────┘
         │                                     │                │
    ┌────▼─────┐                       ┌───────▼──────┐  ┌──────▼────┐
    │ S3/GCS   │                       │ Redis Cache  │  │ User DB   │
    │ (Photos) │                       └───────┬──────┘  │ (Postgres)│
    └──────────┘                               │         └───────────┘
                                        ┌──────▼─────┐
                                        │ Feed DB    │
                                        │ (Cassandra)│
                                        └────────────┘
```

**Service Responsibilities**
- **Upload Service**: Validate, resize, store photos; emit events
- **Feed Service**: Generate personalized feeds from followed users
- **User Service**: Authentication, profile management, followers

### 4. API Design

**RESTful API Example**
```
POST /api/v1/photos
  - Upload photo
  - Request: multipart/form-data (image file, caption, tags)
  - Response: { photo_id, url, thumbnail_url, created_at }

GET /api/v1/feed
  - Get personalized feed
  - Query params: ?page=1&limit=20
  - Response: { photos: [...], next_page_token }

POST /api/v1/photos/{photo_id}/like
  - Like a photo
  - Response: { liked: true, like_count: 1234 }

GET /api/v1/users/{user_id}
  - Get user profile
  - Response: { user_id, username, bio, follower_count, ... }
```

**API Design Principles**
- **Versioning**: /api/v1/ for backward compatibility
- **Pagination**: Cursor or offset-based for large datasets
- **Rate limiting**: Prevent abuse (e.g., 1000 requests/hour per user)
- **Idempotency**: POST with idempotency keys for safe retries
- **Error handling**: Consistent error format (RFC 7807 Problem Details)

## Trade-Offs & Design Decisions

### CAP Theorem

**Theorem**: In a distributed system, you can only guarantee 2 of 3:
- **Consistency (C)**: All nodes see the same data at the same time
- **Availability (A)**: Every request receives a response (success or failure)
- **Partition Tolerance (P)**: System continues despite network partitions

**In Practice**: Network partitions happen, so choose between CP or AP.

**CP Systems (Consistency + Partition Tolerance)**
- Sacrifice availability during partitions
- Examples: HBase, MongoDB (default), Redis (single master), Spanner
- Use when: Banking, inventory management, strong consistency required
- Trade-off: System may reject requests during network issues

**AP Systems (Availability + Partition Tolerance)**
- Sacrifice consistency (eventual consistency)
- Examples: Cassandra, DynamoDB, Riak, CouchDB
- Use when: Social media feeds, recommendations, analytics
- Trade-off: Users may see stale data temporarily

**Real-World Example: E-Commerce Inventory**
- **CP approach**: Show "out of stock" if can't verify inventory across all regions
- **AP approach**: Risk overselling, reconcile later with cancellations

### PACELC Extension

**PACELC**: If Partition, choose A or C; Else (no partition), choose Latency or Consistency.

- **PA/EL**: DynamoDB (available during partition, low latency normally)
- **PC/EC**: HBase (consistent during partition, consistent normally)
- **PA/EC**: Cassandra (configurable: available + tunable consistency)

### Consistency Models

**Strong Consistency**
- Read always returns most recent write
- Examples: ACID databases, Spanner
- Cost: Higher latency, lower availability

**Eventual Consistency**
- Reads may return stale data temporarily, eventually converge
- Examples: DNS, Cassandra, DynamoDB
- Benefit: Higher availability, lower latency

**Causal Consistency**
- Preserves cause-effect order (if A → B, all nodes see A before B)
- Examples: Some distributed databases
- Middle ground between strong and eventual

### Latency vs Throughput

**Latency**: Time to complete one request
**Throughput**: Number of requests completed per unit time

**Trade-off**: Optimizing for one can hurt the other.
- **Batching**: Increases throughput (process 100 requests together) but increases latency (wait for batch to fill)
- **Caching**: Reduces latency (fast lookups) and increases throughput (fewer DB hits)
- **Async processing**: Improves throughput (handle more concurrent requests) but may increase perceived latency

### Synchronous vs Asynchronous

**Synchronous (Request-Response)**
- Client waits for response
- Simple, easy to reason about
- Limited concurrency, higher latency
- Use for: Critical path operations, real-time needs

**Asynchronous (Message Queue)**
- Fire-and-forget, client doesn't wait
- Higher throughput, better resilience
- Complexity in error handling, eventual consistency
- Use for: Background jobs, non-critical path

## Real-World Design Examples

### Example 1: Design Twitter-Like System

**Requirements**
- Post tweets (280 characters, optional media)
- Follow other users
- View timeline of followed users' tweets
- 100M DAU, 500M tweets/day, 10B timeline reads/day

**Design Decisions**

**1. Data Model**
```sql
-- PostgreSQL for user data (relational)
users (id, username, bio, created_at)
follows (follower_id, followee_id, created_at)

-- Cassandra for tweets (high write throughput)
tweets (tweet_id, user_id, content, media_url, created_at)
  - Partition by user_id for write efficiency

-- Redis for timelines (low latency reads)
timeline:user:{user_id} -> sorted set of tweet_ids by timestamp
```

**2. Tweet Flow**
```
User posts tweet
  → API Gateway
  → Tweet Service writes to Cassandra
  → Publish event to Kafka
  → Timeline Service (fan-out-on-write for users with <10K followers)
     - Add tweet to followers' Redis timelines
  → For celebrities (>10K followers), use fan-out-on-read
     - Generate timeline on-demand by merging followed users' tweets
```

**3. Scaling Strategy**
- Shard tweets by user_id across 100 Cassandra nodes
- Cache timelines in Redis (1M most active users, 30-day TTL)
- CDN for media files
- Read replicas for user database (10:1 read/write ratio)

### Example 2: Design URL Shortener (like bit.ly)

**Requirements**
- Shorten long URL to short code (e.g., bit.ly/abc123)
- Redirect short URL to original URL
- 1M new URLs/day, 100M redirects/day
- Analytics (click counts, geographic data)

**Design**

**1. Short Code Generation**
```python
# Base62 encoding (a-z, A-Z, 0-9) = 62^7 ≈ 3.5 trillion combinations
def encode_id(id: int) -> str:
    """Convert ID to base62 short code"""
    chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    code = ""
    while id > 0:
        code = chars[id % 62] + code
        id //= 62
    return code.rjust(7, '0')  # 7-character code

# ID from auto-increment database or distributed ID generator (Snowflake)
```

**2. Architecture**
```
┌────────┐        ┌──────────────┐        ┌─────────────┐
│ Client │ ─────> │ Load Balancer│ ─────> │ API Service │
└────────┘        └──────────────┘        └──────┬──────┘
                                                  │
                  ┌───────────────────────────────┼────────────────┐
                  │                               │                │
           ┌──────▼──────┐              ┌─────────▼────────┐ ┌─────▼─────┐
           │ Redis Cache │              │ PostgreSQL       │ │ Analytics │
           │ (url_map)   │              │ (url_id, url,    │ │ Service   │
           └─────────────┘              │  created_at)     │ │ (Kafka)   │
                                        └──────────────────┘ └───────────┘
```

**3. Redirect Flow (Hot Path)**
```
GET bit.ly/abc123
  → Check Redis cache
  → Cache hit: redirect (99% case, <10ms)
  → Cache miss: query database → update cache → redirect
  → Async: publish click event to Kafka for analytics
```

**4. Optimization**
- Cache 100K most popular URLs in Redis
- Database read replicas for redundancy
- Pregenerate short codes during low traffic
- Use CDN for redirects (additional caching layer)

### Example 3: Design Uber-Like Ride-Sharing System

**Requirements**
- Match riders with nearby drivers
- Real-time location tracking
- Pricing based on distance, time, demand
- 10M rides/day, 1M active drivers, 5M active riders

**Design Decisions**

**1. Geospatial Indexing**
```
# QuadTree or Geohash for location indexing
- Divide map into grid cells
- Store driver locations in Redis Geospatial index
- Query: GEORADIUS 37.7749 -122.4194 5 km
  → Returns drivers within 5km radius
```

**2. Matching Algorithm**
```
Rider requests ride
  → Query nearby drivers (Redis GEORADIUS)
  → Filter: driver available, rating >4.5, accepts ride type
  → Rank: distance, driver rating, acceptance rate
  → Send ride request to top 3 drivers
  → First to accept wins (optimistic concurrency)
```

**3. Real-Time Location Tracking**
```
Driver app → WebSocket connection → Location Service
  → Update Redis every 5 seconds
  → Update database every 30 seconds (for analytics)
  → Publish location events to Kafka (for rider app updates)
```

**4. Pricing Service**
```
Base fare + (distance × per_km_rate) + (time × per_min_rate) + surge_multiplier

Surge pricing:
  - Calculate supply/demand ratio per region every 5 minutes
  - High demand + low supply → increase multiplier (1.5x, 2x, 3x)
  - Store in Redis, cache on client
```

**5. Architecture Highlights**
- **Microservices**: Rider, Driver, Matching, Pricing, Notification, Payment
- **Databases**: PostgreSQL (users, rides), Redis (live locations, pricing), Cassandra (trip history)
- **Message Queue**: Kafka for events (ride_requested, driver_matched, trip_completed)
- **Real-time**: WebSockets for live location, ride status updates

## Design Checklist

### Before Starting
- [ ] Clarify functional requirements (what features?)
- [ ] Clarify non-functional requirements (scale, performance, availability)
- [ ] Estimate scale (users, requests/sec, data volume)
- [ ] Identify read-heavy vs write-heavy workload
- [ ] Determine consistency requirements (strong vs eventual)

### High-Level Design
- [ ] Define API contracts (REST/GraphQL/gRPC)
- [ ] Choose architecture pattern (monolith/microservices/serverless)
- [ ] Identify core services and their responsibilities
- [ ] Design data model and choose databases
- [ ] Plan for caching strategy
- [ ] Design inter-service communication (sync/async)

### Detailed Design
- [ ] Database schema (tables, indexes, partitioning)
- [ ] Sharding strategy if needed (shard key, rebalancing)
- [ ] Caching strategy (what to cache, TTL, eviction policy)
- [ ] Load balancing (L4/L7, algorithm, health checks)
- [ ] Message queues (topics, retention, ordering guarantees)
- [ ] CDN for static assets and geographic distribution

### Reliability & Operations
- [ ] Single points of failure identified and mitigated
- [ ] Replication strategy (master-slave, multi-master)
- [ ] Backup and disaster recovery plan
- [ ] Monitoring and alerting (metrics, logs, traces)
- [ ] Rate limiting and DDoS protection
- [ ] Security (authentication, authorization, encryption)

### Optimization
- [ ] Identify bottlenecks (database queries, network calls)
- [ ] Database indexing strategy
- [ ] Async processing for non-critical tasks
- [ ] Connection pooling for databases
- [ ] Compression for large payloads
- [ ] Pagination for large result sets

## Common Mistakes

### 1. Over-Engineering
**Mistake**: Building for 1M users when you have 100.
**Fix**: Start simple (monolith, single database), scale when needed.
**Rule of thumb**: Optimize for time-to-market first, then scale.

### 2. Premature Optimization
**Mistake**: Optimizing before measuring, guessing bottlenecks.
**Fix**: Measure first (profiling, monitoring), then optimize.
**Quote**: "Premature optimization is the root of all evil" - Donald Knuth

### 3. Single Points of Failure
**Mistake**: Single database, single API server, no backups.
**Fix**: Redundancy at every layer (load balancer, app servers, database replicas).
**Examples**: Multi-AZ deployment, database replication, regular backups

### 4. Ignoring Network Reliability
**Mistake**: Assuming network calls always succeed.
**Fix**: Implement retries, timeouts, circuit breakers, fallbacks.
**Fallacies**: "The network is reliable", "Latency is zero", "Bandwidth is infinite"

### 5. Not Planning for Failure
**Mistake**: No graceful degradation, no error handling strategy.
**Fix**: Design for failure (chaos engineering), test failure scenarios.
**Examples**: Return cached data if DB is down, show static page if API fails

### 6. Poor Database Design
**Mistake**: No indexes, inefficient queries, no partitioning strategy.
**Fix**: Index foreign keys and query columns, use EXPLAIN, partition large tables.
**Anti-pattern**: SELECT * from million-row table without WHERE clause

### 7. Tight Coupling
**Mistake**: Services directly depend on each other's internal implementation.
**Fix**: Well-defined APIs, event-driven architecture, API versioning.
**Benefit**: Independent deployment, easier testing, team autonomy

### 8. Insufficient Monitoring
**Mistake**: No visibility into system health, find out about issues from users.
**Fix**: Comprehensive monitoring (metrics, logs, traces), alerting, dashboards.
**Tools**: Prometheus, Grafana, ELK stack, Datadog, New Relic

### 9. Ignoring Security
**Mistake**: No authentication, plaintext passwords, SQL injection vulnerabilities.
**Fix**: Defense in depth (auth, authorization, input validation, encryption, auditing).
**Basics**: HTTPS, password hashing, prepared statements, rate limiting

### 10. Not Considering Costs
**Mistake**: Over-provisioning resources, inefficient queries, no cost monitoring.
**Fix**: Right-size instances, use auto-scaling, monitor cloud costs, optimize queries.
**Example**: Use spot instances for batch jobs, archive old data to cheaper storage

## Success Criteria

Your design is successful when:
- **Meets requirements**: Handles specified load, latency, availability targets
- **Scalable**: Can grow 10x with predictable cost and complexity
- **Reliable**: Handles failures gracefully, no single points of failure
- **Maintainable**: Clear architecture, documented decisions, observable system
- **Cost-effective**: Balanced resource usage, optimized for workload
- **Secure**: Authentication, authorization, encryption, input validation
- **Testable**: Can verify behavior, simulate failures, measure performance

## Related Skills

- **dev-scalability-patterns**: Specific code patterns for scaling applications
- **api-design**: Detailed API design principles and best practices
- **database-design**: Schema design, indexing, query optimization
- **microservices-design-patterns**: Service decomposition, communication patterns
- **caching-strategies**: Cache layers, eviction policies, cache invalidation
- **event-driven**: Event sourcing, CQRS, message queue patterns
- **infrastructure-code**: Terraform, CloudFormation, Kubernetes deployments

## References

### Essential Reading
- **Designing Data-Intensive Applications** by Martin Kleppmann
  - Comprehensive guide to distributed systems, databases, streaming
  - Covers replication, partitioning, transactions, consistency models

- **System Design Primer** (GitHub)
  - https://github.com/donnemartin/system-design-primer
  - Open-source guide with examples, diagrams, Anki flashcards

- **Grokking the System Design Interview** (DesignGurus)
  - https://www.designgurus.io/course/grokking-the-system-design-interview
  - Real interview questions with detailed solutions

### Latest Resources (2024)
- **Microservices Design Patterns** (Microsoft Azure)
  - https://learn.microsoft.com/en-us/azure/architecture/microservices/design/
  - Patterns for resilience, communication, data management

- **CAP Theorem for System Design Interviews** (DesignGurus)
  - https://www.designgurus.io/answers/detail/cap-theorem-for-system-design-interview
  - Practical guide with database examples

- **GeeksforGeeks System Design Guide**
  - https://www.geeksforgeeks.org/system-design-tutorial/
  - Comprehensive tutorials on scalability, databases, caching

### Tools & Technologies
- **Load Balancers**: Nginx, HAProxy, AWS ALB/NLB, Envoy
- **Caching**: Redis, Memcached, Varnish
- **Databases**: PostgreSQL, MongoDB, Cassandra, DynamoDB
- **Message Queues**: Kafka, RabbitMQ, AWS SQS/SNS, Google Pub/Sub
- **Monitoring**: Prometheus, Grafana, Datadog, New Relic
- **API Gateways**: Kong, Apigee, AWS API Gateway, Tyk

### Practice Resources
- **HelloInterview System Design Course**
  - https://www.hellointerview.com/learn/system-design
  - Deep dives on CAP theorem, load balancing, caching

- **Educative.io System Design Courses**
  - Interactive learning with hands-on exercises
  - Covers design patterns, case studies, interview prep

- **ByteByteGo Newsletter** (Alex Xu)
  - Weekly system design topics with visual explanations
  - Author of "System Design Interview" books
