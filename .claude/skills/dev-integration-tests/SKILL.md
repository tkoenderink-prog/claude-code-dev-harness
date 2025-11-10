---
name: integration-tests
description: Use when working with integration testing in your project - provides testing best practices and implementation patterns
---

# Integration Tests

## When to Use
Use this skill when implementing integration tests that verify multiple components working together, testing API endpoints, database interactions, or external service integrations. Integration tests sit between unit tests and end-to-end tests in the testing pyramid.

## What is Integration Testing?

### Testing Pyramid
```
         /\
        /E2E\       <- Few, slow, expensive (GUI, full system)
       /------\
      /Integration\ <- Some, moderate speed (API, DB, services)
     /------------\
    /  Unit Tests  \ <- Many, fast, cheap (functions, classes)
   /----------------\
```

**Unit Tests**: Test individual functions/classes in isolation with mocked dependencies
**Integration Tests**: Test how multiple components work together with real dependencies
**E2E Tests**: Test complete user workflows through the entire system

### Integration Test Characteristics
- Test multiple components together (API + Database, Service + Queue)
- Use real dependencies when possible (actual DB, not mocks)
- Verify contracts between services
- Test data flow across boundaries
- Slower than unit tests, faster than E2E tests
- Run in isolated test environments

## Test Strategies

### 1. Top-Down Integration
Start with high-level modules, stub lower-level dependencies, integrate downward.
**Use when**: UI-first development, early API contract validation

### 2. Bottom-Up Integration
Start with low-level modules, build upward toward high-level components.
**Use when**: Database-first development, infrastructure-heavy projects

### 3. Big Bang Integration
Integrate all components at once and test as a whole.
**Use when**: Small projects, tight timelines (risky for large systems)

### 4. Incremental Integration (Recommended)
Integrate and test components gradually, one at a time.
**Use when**: Most projects - provides best balance of coverage and debugging ease

## Environment Setup

### Docker Compose for Test Environment
```yaml
# docker-compose.test.yml
version: '3.8'

services:
  test-db:
    image: postgres:16
    environment:
      POSTGRES_DB: test_db
      POSTGRES_USER: test_user
      POSTGRES_PASSWORD: test_password
    ports:
      - "5433:5432"  # Use different port to avoid conflicts
    tmpfs:
      - /var/lib/postgresql/data  # Use tmpfs for speed

  test-redis:
    image: redis:7-alpine
    ports:
      - "6380:6379"

  test-api:
    build: .
    environment:
      DATABASE_URL: postgresql://test_user:test_password@test-db:5432/test_db
      REDIS_URL: redis://test-redis:6379
      ENVIRONMENT: test
    depends_on:
      - test-db
      - test-redis
    command: pytest tests/integration
```

### Testcontainers (2024 Best Practice)
**Python Example**:
```python
# conftest.py
import pytest
from testcontainers.postgres import PostgresContainer
from testcontainers.redis import RedisContainer

@pytest.fixture(scope="session")
def postgres_container():
    """Start PostgreSQL in container for entire test session"""
    with PostgresContainer("postgres:16") as postgres:
        yield postgres

@pytest.fixture(scope="session")
def redis_container():
    """Start Redis in container for entire test session"""
    with RedisContainer("redis:7-alpine") as redis:
        yield redis

@pytest.fixture(scope="function")
def db_connection(postgres_container):
    """Provide fresh DB connection for each test"""
    import psycopg2

    conn = psycopg2.connect(postgres_container.get_connection_url())

    # Setup: Create tables
    with conn.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                email VARCHAR(255) UNIQUE NOT NULL,
                name VARCHAR(255)
            )
        """)
        conn.commit()

    yield conn

    # Teardown: Clean up data
    with conn.cursor() as cursor:
        cursor.execute("TRUNCATE users RESTART IDENTITY CASCADE")
        conn.commit()

    conn.close()
```

**JavaScript/Node.js Example**:
```javascript
// jest.config.js with Testcontainers
const { GenericContainer } = require('testcontainers');

module.exports = {
  globalSetup: './tests/setup.js',
  globalTeardown: './tests/teardown.js',
};

// tests/setup.js
const { PostgreSqlContainer } = require('@testcontainers/postgresql');

module.exports = async () => {
  const container = await new PostgreSqlContainer('postgres:16')
    .withExposedPorts(5432)
    .start();

  global.__POSTGRES_CONTAINER__ = container;
  process.env.DATABASE_URL = container.getConnectionUri();
};

// tests/teardown.js
module.exports = async () => {
  await global.__POSTGRES_CONTAINER__.stop();
};
```

### Key Testcontainers Best Practices (2024)
1. **Never use fixed ports** - Always use dynamic port assignment
2. **Pin image versions** - Use `postgres:16`, not `postgres:latest`
3. **Inject configuration dynamically** - Read host/port from container
4. **Use tmpfs for databases** - Faster test execution
5. **Session-scoped containers** - Start once per test run, not per test

## Database Testing

### Test Data Management Strategies

#### 1. Transaction Rollback Pattern
```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

@pytest.fixture(scope="function")
def db_session(postgres_container):
    """Provide DB session that rolls back after each test"""
    engine = create_engine(postgres_container.get_connection_url())
    Session = sessionmaker(bind=engine)

    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    yield session

    # Rollback transaction - no changes persist
    session.close()
    transaction.rollback()
    connection.close()
```

**Pros**: Fast, automatic cleanup, test isolation
**Cons**: Doesn't catch transaction-commit issues (e.g., uniqueness constraints)

#### 2. Table Truncation Pattern
```python
@pytest.fixture(scope="function")
def clean_database(db_session):
    """Clean all tables before each test"""
    yield  # Test runs here

    # Cleanup after test
    db_session.execute("TRUNCATE users, orders, products RESTART IDENTITY CASCADE")
    db_session.commit()
```

**Pros**: Tests real commits, catches constraint violations
**Cons**: Slower than rollback, must manage foreign key order

#### 3. Schema Isolation Pattern
```python
@pytest.fixture(scope="function")
def isolated_schema(postgres_container):
    """Create separate schema for each test"""
    import uuid
    schema_name = f"test_{uuid.uuid4().hex[:8]}"

    engine = create_engine(postgres_container.get_connection_url())
    with engine.connect() as conn:
        conn.execute(f"CREATE SCHEMA {schema_name}")
        conn.execute(f"SET search_path TO {schema_name}")
        # Run migrations in this schema
        run_migrations(conn, schema_name)

    yield engine

    with engine.connect() as conn:
        conn.execute(f"DROP SCHEMA {schema_name} CASCADE")
```

**Pros**: Complete isolation, parallel test execution
**Cons**: Schema creation overhead (~50ms per test)

### Test Factories and Fixtures
```python
# factories.py
import factory
from factory.alchemy import SQLAlchemyModelFactory
from models import User, Order

class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = None  # Set in fixture

    email = factory.Sequence(lambda n: f"user{n}@example.com")
    name = factory.Faker('name')
    is_active = True

class OrderFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Order
        sqlalchemy_session = None

    user = factory.SubFactory(UserFactory)
    total = factory.Faker('pydecimal', left_digits=3, right_digits=2, positive=True)
    status = "pending"

# test_orders.py
def test_order_creation(db_session):
    # Arrange
    UserFactory._meta.sqlalchemy_session = db_session
    OrderFactory._meta.sqlalchemy_session = db_session

    user = UserFactory.create(email="john@example.com")

    # Act
    order = OrderFactory.create(user=user, total=99.99)

    # Assert
    assert order.user.email == "john@example.com"
    assert order.total == 99.99
    assert order.status == "pending"
```

## API Testing

### REST API Integration Tests

```python
# test_api.py
import pytest
from fastapi.testclient import TestClient
from app import create_app

@pytest.fixture
def api_client(db_session):
    """API client with test database"""
    app = create_app(database_session=db_session)
    return TestClient(app)

def test_create_user_api(api_client):
    # Arrange
    user_data = {
        "email": "test@example.com",
        "name": "Test User"
    }

    # Act
    response = api_client.post("/api/users", json=user_data)

    # Assert
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data

def test_get_user_api(api_client, db_session):
    # Arrange - Create user via factory
    user = UserFactory.create(db_session=db_session)

    # Act
    response = api_client.get(f"/api/users/{user.id}")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user.id
    assert data["email"] == user.email

def test_user_not_found(api_client):
    # Act
    response = api_client.get("/api/users/99999")

    # Assert
    assert response.status_code == 404
    assert response.json()["error"] == "User not found"
```

### GraphQL API Testing
```python
def test_graphql_query(api_client, db_session):
    # Arrange
    user = UserFactory.create(db_session=db_session, name="Alice")

    query = """
        query GetUser($id: ID!) {
            user(id: $id) {
                id
                name
                email
            }
        }
    """

    # Act
    response = api_client.post("/graphql", json={
        "query": query,
        "variables": {"id": str(user.id)}
    })

    # Assert
    assert response.status_code == 200
    data = response.json()["data"]["user"]
    assert data["name"] == "Alice"
```

### Mocking External APIs
```python
import responses
from requests.exceptions import HTTPError

@responses.activate
def test_external_api_integration(api_client):
    # Arrange - Mock external payment API
    responses.add(
        responses.POST,
        "https://payment-api.example.com/charge",
        json={"transaction_id": "txn_123", "status": "success"},
        status=200
    )

    # Act - Call our API which calls external API
    response = api_client.post("/api/orders", json={
        "user_id": 1,
        "amount": 50.00
    })

    # Assert
    assert response.status_code == 201
    assert response.json()["payment_status"] == "success"
    assert len(responses.calls) == 1  # Verify external API was called

@responses.activate
def test_external_api_failure_handling(api_client):
    # Arrange - Mock external API failure
    responses.add(
        responses.POST,
        "https://payment-api.example.com/charge",
        json={"error": "Card declined"},
        status=402
    )

    # Act
    response = api_client.post("/api/orders", json={
        "user_id": 1,
        "amount": 50.00
    })

    # Assert - Verify graceful error handling
    assert response.status_code == 402
    assert "Card declined" in response.json()["error"]
```

## Authentication in Integration Tests

### JWT Token Fixtures
```python
# conftest.py
import jwt
from datetime import datetime, timedelta

@pytest.fixture
def auth_token():
    """Generate valid JWT token for tests"""
    payload = {
        "user_id": 1,
        "email": "test@example.com",
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    return jwt.encode(payload, "test-secret-key", algorithm="HS256")

@pytest.fixture
def authenticated_client(api_client, auth_token):
    """API client with authentication header"""
    api_client.headers["Authorization"] = f"Bearer {auth_token}"
    return api_client

# test_protected_endpoints.py
def test_protected_endpoint(authenticated_client, db_session):
    # Arrange
    user = UserFactory.create(id=1, db_session=db_session)

    # Act - Call protected endpoint
    response = authenticated_client.get("/api/profile")

    # Assert
    assert response.status_code == 200
    assert response.json()["email"] == user.email

def test_unauthenticated_access_denied(api_client):
    # Act - Call protected endpoint without auth
    response = api_client.get("/api/profile")

    # Assert
    assert response.status_code == 401
    assert "Unauthorized" in response.json()["error"]
```

### Bypassing Authentication in Tests
```python
# app/dependencies.py
def get_current_user(token: str = Depends(oauth2_scheme)):
    """Dependency that extracts user from JWT token"""
    if os.getenv("TESTING"):
        # In test mode, use test user
        return User(id=1, email="test@example.com")
    # Normal authentication logic
    return verify_token(token)

# Alternative: Override dependency in tests
def test_with_dependency_override(api_client):
    # Arrange - Override auth dependency
    def override_get_current_user():
        return User(id=1, email="test@example.com", is_admin=True)

    app.dependency_overrides[get_current_user] = override_get_current_user

    # Act
    response = api_client.get("/api/admin/users")

    # Assert
    assert response.status_code == 200

    # Cleanup
    app.dependency_overrides.clear()
```

## Mocking vs Real Dependencies

### When to Mock
✅ **Mock when**:
- External paid services (payment gateways, SMS providers)
- Third-party APIs with rate limits
- Services outside your control (weather API, stock prices)
- Slow external services (legacy SOAP APIs)
- Testing error scenarios (network failures, timeouts)

### When to Use Real Dependencies
✅ **Use real when**:
- Your own databases (use Testcontainers)
- Your own microservices
- Message queues (Kafka, RabbitMQ in containers)
- Cache layers (Redis, Memcached)
- Search engines (Elasticsearch, OpenSearch)

### Example: Mixed Approach
```python
def test_order_processing_integration(
    db_session,          # Real database
    redis_client,        # Real Redis
    mock_payment_api,    # Mocked external service
    mock_email_service   # Mocked external service
):
    # Arrange
    user = UserFactory.create(db_session=db_session)

    # Act - Process order (uses real DB/Redis, mocked externals)
    order = process_order(user.id, items=[{"id": 1, "qty": 2}])

    # Assert
    assert order.status == "confirmed"  # From real DB
    assert redis_client.get(f"order:{order.id}") is not None  # Real cache
    mock_payment_api.assert_called_once()  # Mocked external
    mock_email_service.assert_called_with(user.email)  # Mocked external
```

## Test Isolation and Parallel Execution

### Ensuring Test Isolation
```python
# pytest.ini
[pytest]
addopts = -n auto  # Parallel execution with pytest-xdist

# conftest.py - Worker-specific resources
@pytest.fixture(scope="session")
def postgres_container(worker_id):
    """Each pytest worker gets own database"""
    if worker_id == "master":
        # Non-parallel run
        db_name = "test_db"
    else:
        # Parallel run - unique DB per worker
        db_name = f"test_db_{worker_id}"

    with PostgresContainer("postgres:16") as postgres:
        # Create database
        postgres.exec(f"createdb {db_name}")
        yield postgres.with_env("POSTGRES_DB", db_name)
```

### Cleanup Strategies Comparison
```python
# Strategy 1: Transaction Rollback (Fastest)
# Time: ~5ms per test
@pytest.fixture
def db_transaction(engine):
    connection = engine.connect()
    transaction = connection.begin()
    yield connection
    transaction.rollback()

# Strategy 2: Table Truncation (Balanced)
# Time: ~50ms per test
@pytest.fixture
def clean_tables(db_session):
    yield
    for table in reversed(metadata.sorted_tables):
        db_session.execute(table.delete())
    db_session.commit()

# Strategy 3: Database Recreation (Slowest but most isolated)
# Time: ~200ms per test
@pytest.fixture
def fresh_database():
    create_database()
    run_migrations()
    yield
    drop_database()
```

## CI/CD Integration

### GitHub Actions Example
```yaml
# .github/workflows/integration-tests.yml
name: Integration Tests

on: [push, pull_request]

jobs:
  integration-tests:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

      redis:
        image: redis:7-alpine
        ports:
          - 6379:6379

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov

      - name: Run integration tests
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test_db
          REDIS_URL: redis://localhost:6379
        run: |
          pytest tests/integration -v --cov --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

### Docker-in-Docker for Testcontainers
```yaml
# For Testcontainers in CI
jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Run integration tests with Testcontainers
        run: |
          # Testcontainers will automatically use GitHub Actions Docker
          pytest tests/integration
        env:
          # Testcontainers Cloud (optional, for faster CI)
          TESTCONTAINERS_CLOUD_TOKEN: ${{ secrets.TC_CLOUD_TOKEN }}
```

## Common Patterns

### AAA Pattern (Arrange-Act-Assert)
```python
def test_user_registration_flow(api_client, db_session):
    # Arrange - Set up test data and state
    user_data = {
        "email": "newuser@example.com",
        "password": "SecurePass123!",
        "name": "New User"
    }

    # Act - Perform the action being tested
    response = api_client.post("/api/register", json=user_data)

    # Assert - Verify the expected outcome
    assert response.status_code == 201
    assert response.json()["email"] == user_data["email"]

    # Assert side effects
    user = db_session.query(User).filter_by(email=user_data["email"]).first()
    assert user is not None
    assert user.is_active is True
```

### Builder Pattern for Complex Test Data
```python
class OrderBuilder:
    def __init__(self, db_session):
        self.db_session = db_session
        self.user = None
        self.items = []
        self.status = "pending"

    def for_user(self, user):
        self.user = user
        return self

    def with_items(self, items):
        self.items = items
        return self

    def with_status(self, status):
        self.status = status
        return self

    def build(self):
        order = Order(user=self.user, status=self.status)
        self.db_session.add(order)
        for item in self.items:
            order_item = OrderItem(order=order, **item)
            self.db_session.add(order_item)
        self.db_session.commit()
        return order

# Usage
def test_order_total_calculation(db_session):
    user = UserFactory.create(db_session=db_session)

    order = (OrderBuilder(db_session)
        .for_user(user)
        .with_items([
            {"product_id": 1, "quantity": 2, "price": 10.00},
            {"product_id": 2, "quantity": 1, "price": 25.00}
        ])
        .build())

    assert order.total == 45.00
```

## Tools and Frameworks

### Python
- **pytest**: Primary testing framework
- **testcontainers-python**: Docker containers for tests
- **factory-boy**: Test data factories
- **responses**: HTTP mock library
- **pytest-xdist**: Parallel test execution
- **httpx/TestClient**: FastAPI testing

### JavaScript/Node.js
- **Jest**: Testing framework with built-in mocking
- **@testcontainers/node**: Testcontainers for Node.js
- **supertest**: HTTP assertions
- **nock**: HTTP mocking
- **faker-js**: Generate fake data

### Tools
- **Docker Compose**: Multi-container test environments
- **Testcontainers**: Programmatic container management
- **WireMock**: API mocking server
- **Localstack**: Mock AWS services

## Success Criteria

✅ **Integration tests should**:
- Use real dependencies when possible (database, cache, queues)
- Mock external services outside your control
- Run in isolated environments (containers, schemas)
- Clean up after themselves (rollback, truncate, drop)
- Run in CI/CD pipelines reliably
- Execute in parallel without conflicts
- Cover critical integration points
- Test error scenarios and edge cases
- Maintain reasonable execution time (< 5 min for full suite)

## Common Pitfalls

❌ **Avoid**:
- Using production databases for tests
- Fixed ports causing conflicts (use dynamic ports)
- Shared test data across tests (causes flakiness)
- Not cleaning up test data (pollutes DB)
- Over-mocking (defeats integration test purpose)
- Testing too many things in one test
- Ignoring transaction commit behavior
- Hardcoded configuration (use environment variables)

## Related Skills

- `test-driven-development` - TDD workflow for integration tests
- `e2e-tests` - Full system end-to-end testing
- `api-design` - Designing testable APIs
- `docker-patterns` - Container patterns for testing
- `debugging-tools` - Debugging failing integration tests
- `ci-setup` - CI/CD pipeline configuration

## References

- [Testcontainers Documentation](https://testcontainers.com/) - Official Testcontainers guide
- [Testcontainers Best Practices](https://www.docker.com/blog/testcontainers-best-practices/) - Docker's 2024 guide
- [Pytest Documentation](https://docs.pytest.org/) - Pytest fixtures and patterns
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/) - Testing FastAPI applications
- [Testing Pyramid](https://martinfowler.com/articles/practical-test-pyramid.html) - Martin Fowler's guide
- [Integration Testing Strategies](https://lostechies.com/jimmybogard/2013/06/18/strategies-for-isolating-the-database-in-tests/) - Database isolation patterns
