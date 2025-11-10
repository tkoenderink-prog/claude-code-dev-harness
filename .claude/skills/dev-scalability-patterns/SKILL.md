---
name: dev-scalability-patterns
description: Use when working with scaling strategies in your project - provides architecture best practices and implementation patterns
---

# Scalability Patterns

## When to Use
Use this skill when you need to:
- Scale your application to handle increased traffic or data volume
- Design systems that can grow from 100 to 10M+ users
- Optimize performance for high-throughput applications
- Reduce latency and improve response times
- Implement cost-effective scaling strategies
- Design for horizontal or vertical growth

Trigger phrases: "scaling", "performance optimization", "high traffic", "load balancing", "database scaling", "caching layer"

## Core Scaling Strategies

### 1. Vertical vs Horizontal Scaling

#### Vertical Scaling (Scale Up)
**Definition**: Adding more resources (CPU, RAM, storage) to existing servers.

**When to Use**:
- Single-threaded applications
- Monolithic architectures
- Quick short-term solutions
- Database masters (PostgreSQL, MySQL)
- When simplicity is prioritized

**Pros**:
- Simple implementation (minimal code changes)
- No data consistency issues
- Lower network overhead
- Easier to maintain

**Cons**:
- Hardware limits (physical ceiling)
- Single point of failure
- Downtime during upgrades
- Cost increases exponentially

**Cost Analysis**:
```
1 server: 32 CPU, 128GB RAM = $500/month
vs
10 servers: 4 CPU, 16GB RAM each = $300/month

Vertical: Higher cost, easier management
Horizontal: Lower cost, complex management
```

#### Horizontal Scaling (Scale Out)
**Definition**: Adding more servers/instances to distribute the load.

**When to Use**:
- Stateless applications
- Microservices architectures
- Unpredictable growth patterns
- High availability requirements
- Read-heavy workloads

**Pros**:
- No theoretical limit
- High availability (redundancy)
- Cost-effective at scale
- Rolling deployments (no downtime)

**Cons**:
- Complex application design
- Data synchronization challenges
- Network latency overhead
- Requires load balancing

**Implementation Pattern**:
```yaml
# Docker Compose - Horizontal Scaling
version: '3.8'
services:
  web:
    image: myapp:latest
    deploy:
      replicas: 5
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
    environment:
      - STATELESS=true
      - SESSION_STORE=redis
```

---

## 2. Load Balancing Strategies

### Load Balancer Types

**Layer 4 (Transport Layer)**:
- Routes based on IP/Port
- Faster, lower latency
- Examples: AWS NLB, HAProxy

**Layer 7 (Application Layer)**:
- Routes based on HTTP headers, URLs
- Content-based routing
- Examples: AWS ALB, Nginx, Traefik

### Load Balancing Algorithms

```python
# Round Robin - Simplest approach
servers = ['server1', 'server2', 'server3']
current = 0

def get_next_server():
    global current
    server = servers[current % len(servers)]
    current += 1
    return server

# Weighted Round Robin
servers = [
    {'name': 'server1', 'weight': 5},
    {'name': 'server2', 'weight': 3},
    {'name': 'server3', 'weight': 2}
]

# Least Connections - For long-lived connections
connections = {'server1': 12, 'server2': 8, 'server3': 15}

def get_least_connected():
    return min(connections, key=connections.get)
```

### Nginx Configuration Example
```nginx
upstream backend {
    # Least connections algorithm
    least_conn;

    # Health checks
    server backend1.example.com:8080 max_fails=3 fail_timeout=30s;
    server backend2.example.com:8080 max_fails=3 fail_timeout=30s;
    server backend3.example.com:8080 max_fails=3 fail_timeout=30s;

    # Sticky sessions (IP hash)
    # ip_hash;

    keepalive 32;
}

server {
    listen 80;

    location / {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;

        # Health check endpoint
        proxy_next_upstream error timeout invalid_header http_500;
    }

    # Health check endpoint
    location /health {
        access_log off;
        return 200 "healthy\n";
    }
}
```

**Performance Impact**:
- Round Robin: ~1ms overhead
- Least Connections: ~2ms overhead (tracking required)
- IP Hash: ~1ms overhead (for sticky sessions)

---

## 3. Caching Strategies

### Cache Hierarchy
```
User Request
    ↓
CDN Cache (CloudFront/Cloudflare) - 5-50ms
    ↓
Application Cache (Redis/Memcached) - 1-5ms
    ↓
Database Query Cache - 10-50ms
    ↓
Database - 50-500ms
```

### Redis Implementation Patterns

#### Cache-Aside (Lazy Loading)
```python
import redis
import json
from typing import Optional

redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

def get_user(user_id: int) -> Optional[dict]:
    cache_key = f"user:{user_id}"

    # Try cache first
    cached = redis_client.get(cache_key)
    if cached:
        print(f"Cache HIT for user {user_id}")
        return json.loads(cached)

    # Cache miss - fetch from database
    print(f"Cache MISS for user {user_id}")
    user = db.query(f"SELECT * FROM users WHERE id = {user_id}")

    # Store in cache with TTL
    redis_client.setex(
        cache_key,
        3600,  # 1 hour TTL
        json.dumps(user)
    )

    return user

# Performance:
# Cache hit: ~2ms
# Cache miss: ~150ms (DB query) + ~2ms (cache write)
# Cache hit ratio: Target >95% for effective caching
```

#### Write-Through Pattern
```python
def update_user(user_id: int, data: dict):
    cache_key = f"user:{user_id}"

    # Update database
    db.update("users", user_id, data)

    # Immediately update cache
    redis_client.setex(cache_key, 3600, json.dumps(data))

    return data

# Pros: Cache always consistent
# Cons: Higher write latency (write penalty)
```

#### Write-Behind (Write-Back) Pattern
```python
import asyncio
from queue import Queue

write_queue = Queue()

async def update_user_async(user_id: int, data: dict):
    cache_key = f"user:{user_id}"

    # Update cache immediately
    redis_client.setex(cache_key, 3600, json.dumps(data))

    # Queue database write
    write_queue.put((user_id, data))

    return data

# Background worker
async def process_write_queue():
    while True:
        if not write_queue.empty():
            user_id, data = write_queue.get()
            db.update("users", user_id, data)
        await asyncio.sleep(0.1)

# Pros: Lowest write latency
# Cons: Risk of data loss if cache fails before DB write
```

### Cache Eviction Policies
```redis
# Redis Configuration
maxmemory 2gb
maxmemory-policy allkeys-lru

# Policies:
# allkeys-lru: Evict least recently used (recommended default)
# allkeys-lfu: Evict least frequently used
# volatile-ttl: Evict keys with shortest TTL
# noeviction: Return errors when memory full
```

### CDN Optimization Best Practices

**CloudFront Configuration**:
```json
{
  "DistributionConfig": {
    "Comment": "Production CDN",
    "DefaultCacheBehavior": {
      "MinTTL": 0,
      "DefaultTTL": 86400,
      "MaxTTL": 31536000,
      "Compress": true,
      "ViewerProtocolPolicy": "redirect-to-https"
    },
    "CacheBehaviors": [
      {
        "PathPattern": "/api/*",
        "MinTTL": 0,
        "DefaultTTL": 0
      },
      {
        "PathPattern": "/static/*",
        "MinTTL": 31536000,
        "DefaultTTL": 31536000
      }
    ]
  }
}
```

**Cloudflare Page Rules**:
- Static assets (images, CSS, JS): Cache Everything, Edge TTL 1 year
- API endpoints: Bypass cache
- HTML pages: Cache by device type, Edge TTL 1 hour

**Performance Gains**:
- Without CDN: 500-2000ms (cross-continent)
- With CDN: 5-50ms (edge location)
- Cost reduction: 60-80% bandwidth costs

---

## 4. Database Scaling Patterns

### Read Replicas

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Master database (writes)
master_engine = create_engine('postgresql://master:5432/db')

# Read replicas (reads)
replica_engines = [
    create_engine('postgresql://replica1:5432/db'),
    create_engine('postgresql://replica2:5432/db'),
    create_engine('postgresql://replica3:5432/db')
]

import random

def get_db_session(write=False):
    if write:
        return sessionmaker(bind=master_engine)()
    else:
        # Load balance across replicas
        engine = random.choice(replica_engines)
        return sessionmaker(bind=engine)()

# Usage
def get_user(user_id):
    session = get_db_session(write=False)  # Use replica
    return session.query(User).filter_by(id=user_id).first()

def update_user(user_id, data):
    session = get_db_session(write=True)  # Use master
    user = session.query(User).filter_by(id=user_id).first()
    user.update(data)
    session.commit()
```

**Replication Lag**: Expect 100ms - 5s delay between master and replicas.

### Database Sharding Strategies

#### Range-Based Sharding
```python
# Shard by user ID ranges
def get_shard(user_id: int) -> str:
    if user_id < 1_000_000:
        return 'shard_1'  # Users 0-999,999
    elif user_id < 2_000_000:
        return 'shard_2'  # Users 1M-1.999M
    else:
        return 'shard_3'  # Users 2M+

# Pros: Simple, easy to add shards
# Cons: Uneven distribution (hotspots)
```

#### Hash-Based Sharding
```python
import hashlib

def get_shard(user_id: int, num_shards: int = 4) -> str:
    hash_value = int(hashlib.md5(str(user_id).encode()).hexdigest(), 16)
    shard_num = hash_value % num_shards
    return f'shard_{shard_num}'

# Pros: Even distribution
# Cons: Rebalancing when adding shards is expensive
```

#### Geographic Sharding
```python
SHARD_MAP = {
    'US': 'us-east-db',
    'EU': 'eu-west-db',
    'ASIA': 'ap-southeast-db'
}

def get_shard(user_region: str) -> str:
    return SHARD_MAP.get(user_region, 'us-east-db')

# Pros: Low latency, data sovereignty compliance
# Cons: Uneven load distribution
```

### Partitioning Strategies

```sql
-- Range Partitioning (PostgreSQL)
CREATE TABLE orders (
    id SERIAL,
    order_date DATE,
    amount DECIMAL
) PARTITION BY RANGE (order_date);

CREATE TABLE orders_2024_q1 PARTITION OF orders
    FOR VALUES FROM ('2024-01-01') TO ('2024-04-01');

CREATE TABLE orders_2024_q2 PARTITION OF orders
    FOR VALUES FROM ('2024-04-01') TO ('2024-07-01');

-- Hash Partitioning
CREATE TABLE users (
    id SERIAL,
    email VARCHAR(255)
) PARTITION BY HASH (id);

CREATE TABLE users_0 PARTITION OF users
    FOR VALUES WITH (MODULUS 4, REMAINDER 0);

CREATE TABLE users_1 PARTITION OF users
    FOR VALUES WITH (MODULUS 4, REMAINDER 1);
```

### Connection Pooling

```python
# Python with psycopg2
from psycopg2 import pool

# Create connection pool
connection_pool = pool.SimpleConnectionPool(
    minconn=10,
    maxconn=100,
    host='localhost',
    database='mydb',
    user='user',
    password='password'
)

def execute_query(query):
    conn = connection_pool.getconn()
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()
    finally:
        connection_pool.putconn(conn)

# Performance impact:
# Without pooling: 50-100ms per connection
# With pooling: 1-5ms (connection reuse)
```

---

## 5. Async Processing Patterns

### Message Queue Comparison

| Feature | RabbitMQ | Apache Kafka |
|---------|----------|--------------|
| **Best For** | Task queues, RPC | Event streaming, logs |
| **Message Retention** | Until consumed | Configurable (days/weeks) |
| **Throughput** | ~20K msg/sec | ~1M+ msg/sec |
| **Latency** | <10ms | ~10-50ms |
| **Ordering** | Per queue | Per partition |
| **Use Case** | Microservice communication | Analytics, event sourcing |

### RabbitMQ Implementation

```python
import pika
import json

# Producer
def send_email_task(user_id, email_content):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost')
    )
    channel = connection.channel()

    # Declare queue
    channel.queue_declare(queue='email_tasks', durable=True)

    # Send message
    channel.basic_publish(
        exchange='',
        routing_key='email_tasks',
        body=json.dumps({
            'user_id': user_id,
            'content': email_content
        }),
        properties=pika.BasicProperties(
            delivery_mode=2,  # Persistent message
        )
    )

    connection.close()

# Consumer
def process_email_tasks():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost')
    )
    channel = connection.channel()
    channel.queue_declare(queue='email_tasks', durable=True)

    def callback(ch, method, properties, body):
        task = json.loads(body)
        send_email(task['user_id'], task['content'])
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='email_tasks', on_message_callback=callback)
    channel.start_consuming()

# Benefits:
# - Decouples services
# - Handles traffic spikes
# - Retry failed tasks
# - Scales workers independently
```

### Kafka Implementation

```python
from kafka import KafkaProducer, KafkaConsumer
import json

# Producer - Event streaming
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def log_user_activity(user_id, action):
    producer.send('user-activity', {
        'user_id': user_id,
        'action': action,
        'timestamp': time.time()
    })

# Consumer - Process events
consumer = KafkaConsumer(
    'user-activity',
    bootstrap_servers=['localhost:9092'],
    group_id='analytics-group',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

for message in consumer:
    event = message.value
    # Process event (analytics, aggregation, etc.)
    update_analytics(event)
```

---

## 6. Auto-Scaling Configuration

### Metrics-Based Auto-Scaling

```yaml
# Kubernetes HPA (Horizontal Pod Autoscaler)
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: web-app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: web-app
  minReplicas: 3
  maxReplicas: 50
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Pods
    pods:
      metric:
        name: http_requests_per_second
      target:
        type: AverageValue
        averageValue: "1000"
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300  # 5 min cooldown
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Percent
        value: 100
        periodSeconds: 30
```

### AWS Auto Scaling Configuration

```json
{
  "AutoScalingGroupName": "web-asg",
  "MinSize": 2,
  "MaxSize": 20,
  "DesiredCapacity": 5,
  "HealthCheckGracePeriod": 300,
  "TargetTrackingScalingPolicies": [
    {
      "PolicyName": "cpu-target-tracking",
      "TargetValue": 70.0,
      "PredefinedMetricSpecification": {
        "PredefinedMetricType": "ASGAverageCPUUtilization"
      }
    },
    {
      "PolicyName": "request-count-tracking",
      "TargetValue": 1000.0,
      "PredefinedMetricSpecification": {
        "PredefinedMetricType": "ALBRequestCountPerTarget"
      }
    }
  ]
}
```

---

## 7. Performance Monitoring

### Key Metrics (Four Golden Signals)

1. **Latency**: Time to serve a request
   - Target: P50 < 100ms, P95 < 300ms, P99 < 1s

2. **Traffic**: Requests per second (RPS)
   - Monitor: Current RPS, Peak RPS, Growth trends

3. **Errors**: Rate of failed requests
   - Target: <0.1% error rate

4. **Saturation**: How "full" your service is
   - CPU, Memory, Disk I/O, Network bandwidth

### Monitoring Implementation

```python
from prometheus_client import Counter, Histogram, Gauge
import time

# Define metrics
request_count = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])
request_latency = Histogram('http_request_duration_seconds', 'HTTP request latency', ['endpoint'])
active_connections = Gauge('active_connections', 'Active connections')

def track_request(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()

        try:
            result = func(*args, **kwargs)
            status = 200
        except Exception as e:
            status = 500
            raise
        finally:
            duration = time.time() - start_time
            request_latency.labels(endpoint=func.__name__).observe(duration)
            request_count.labels(method='GET', endpoint=func.__name__, status=status).inc()

        return result
    return wrapper

@track_request
def get_user(user_id):
    # Your application logic
    pass
```

### Latency Percentiles Analysis

```
Example API Performance:
- P50 (median): 45ms     - Half of requests complete under 45ms
- P95: 120ms             - 95% complete under 120ms
- P99: 450ms             - 99% complete under 450ms
- P99.9: 2100ms          - Outliers, investigate bottlenecks

Why P99 matters:
- At 1000 RPS, 10 requests/sec exceed P99
- At 10000 RPS, 100 requests/sec have poor experience
```

---

## Decision Framework

### When to Use Which Pattern

```
Traffic Level          Recommended Approach
──────────────────────────────────────────────
< 100 RPS              Single server + CDN
100 - 1K RPS           Vertical scaling + Redis cache
1K - 10K RPS           Horizontal scaling + Load balancer + Read replicas
10K - 100K RPS         Multi-region + Sharding + Message queues
> 100K RPS             Full distributed system + CDN + Advanced caching
```

### Cost vs Performance Trade-offs

```python
# Cost analysis example
scenarios = {
    'single_large': {
        'servers': 1,
        'cpu': 64,
        'ram': 256,
        'cost_monthly': 800,
        'availability': '99.9%'
    },
    'multiple_medium': {
        'servers': 4,
        'cpu': 16,
        'ram': 64,
        'cost_monthly': 600,
        'availability': '99.99%'
    },
    'many_small': {
        'servers': 16,
        'cpu': 4,
        'ram': 16,
        'cost_monthly': 480,
        'availability': '99.995%'
    }
}

# Recommendation: Start with multiple_medium, scale to many_small
```

---

## Success Criteria

- [ ] Defined target RPS and latency requirements
- [ ] Implemented appropriate caching layer
- [ ] Load balancer configured with health checks
- [ ] Database read/write split implemented
- [ ] Auto-scaling policies configured
- [ ] Monitoring and alerting in place
- [ ] Performance benchmarks documented
- [ ] Cost analysis completed

---

## Common Pitfalls

1. **Premature Optimization**: Don't implement complex scaling before you need it
2. **Ignoring Database**: 80% of bottlenecks are database-related
3. **No Monitoring**: You can't optimize what you don't measure
4. **Cache Invalidation**: One of the hardest problems in CS
5. **Session Stickiness**: Breaks horizontal scaling benefits
6. **No Circuit Breakers**: Cascading failures will take down your system

---

## Related Skills

- `dev-system-design` - High-level architecture patterns
- `database-design` - Schema optimization for scale
- `performance-optimization` - Code-level optimizations
- `cloud-architecture` - Cloud-native scaling patterns
- `monitoring-strategies` - Observability implementation

---

## Tools & Resources

### Load Balancers
- Nginx: https://nginx.org/en/docs/
- HAProxy: https://www.haproxy.org/
- AWS ALB/NLB: https://aws.amazon.com/elasticloadbalancing/

### Caching
- Redis: https://redis.io/docs/
- Memcached: https://memcached.org/
- Varnish: https://varnish-cache.org/

### Message Queues
- RabbitMQ: https://www.rabbitmq.com/documentation.html
- Apache Kafka: https://kafka.apache.org/documentation/
- AWS SQS: https://aws.amazon.com/sqs/

### CDN
- Cloudflare: https://www.cloudflare.com/
- AWS CloudFront: https://aws.amazon.com/cloudfront/
- Fastly: https://www.fastly.com/

### Monitoring
- Prometheus: https://prometheus.io/
- Grafana: https://grafana.com/
- DataDog: https://www.datadoghq.com/
- New Relic: https://newrelic.com/

---

## References

- AWS Well-Architected Framework: https://aws.amazon.com/architecture/well-architected/
- Google SRE Book: https://sre.google/books/
- Martin Fowler - Patterns of Enterprise Application Architecture
- Database Caching Strategies Using Redis (AWS Whitepaper)
- High Scalability Blog: http://highscalability.com/
