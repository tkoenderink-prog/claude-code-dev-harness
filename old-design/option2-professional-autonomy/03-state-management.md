# State & Context System Design

## 1. Overview

The State & Context System enables persistent, intelligent state management across multi-day work sessions. It preserves complete context, enabling the system to resume complex workflows seamlessly and maintain continuity across sessions.

## 2. Architecture Overview

### 2.1 Core Components

```python
class StateManagementSystem:
    """Central state management system"""

    def __init__(self, config: StateConfig):
        # Storage layers
        self.persistent_store = SQLiteStore(config.db_path)
        self.cache_layer = RedisCache(config.redis_config)
        self.memory_store = InMemoryStore(max_size_mb=512)

        # Context management
        self.context_engine = ContextEngine()
        self.context_analyzer = ContextAnalyzer()

        # State synchronization
        self.sync_manager = SyncManager()
        self.conflict_resolver = ConflictResolver()

        # Recovery and backup
        self.recovery_manager = RecoveryManager()
        self.backup_scheduler = BackupScheduler()

        # Performance optimization
        self.query_optimizer = QueryOptimizer()
        self.garbage_collector = GarbageCollector()
```

### 2.2 Storage Architecture Layers

```yaml
storage_layers:
  hot_cache:
    technology: In-Memory LRU Cache
    size: 512MB
    ttl: 5 minutes
    purpose: Ultra-fast access to active state

  warm_cache:
    technology: Redis
    size: 2GB
    ttl: 1 hour
    purpose: Fast access to recent state

  cold_storage:
    technology: SQLite
    size: Unlimited (disk bound)
    ttl: 90 days
    purpose: Persistent state storage

  archive:
    technology: Compressed files
    compression: zstd
    retention: 1 year
    purpose: Long-term state archive
```

## 3. Database Schema Design

### 3.1 Core Tables

```sql
-- Sessions table: Top-level session tracking
CREATE TABLE sessions (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP,
    status TEXT CHECK(status IN ('active', 'paused', 'completed', 'failed')),
    context_snapshot JSONB,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    version INTEGER DEFAULT 1
);

CREATE INDEX idx_sessions_user_id ON sessions(user_id);
CREATE INDEX idx_sessions_status ON sessions(status);
CREATE INDEX idx_sessions_start_time ON sessions(start_time DESC);

-- Tasks table: Individual task tracking
CREATE TABLE tasks (
    id TEXT PRIMARY KEY,
    session_id TEXT REFERENCES sessions(id) ON DELETE CASCADE,
    parent_task_id TEXT REFERENCES tasks(id),
    type TEXT NOT NULL,
    status TEXT CHECK(status IN ('pending', 'in_progress', 'completed', 'failed', 'cancelled')),
    priority INTEGER DEFAULT 5,
    description TEXT,
    parameters JSONB,
    result JSONB,
    error_details JSONB,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    duration_ms INTEGER,
    retry_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_tasks_session_id ON tasks(session_id);
CREATE INDEX idx_tasks_parent_id ON tasks(parent_task_id);
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_type_status ON tasks(type, status);

-- Context table: Contextual information storage
CREATE TABLE context (
    id TEXT PRIMARY KEY,
    session_id TEXT REFERENCES sessions(id) ON DELETE CASCADE,
    context_type TEXT NOT NULL,
    context_key TEXT NOT NULL,
    context_value JSONB NOT NULL,
    relevance_score REAL DEFAULT 1.0,
    access_count INTEGER DEFAULT 0,
    last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(session_id, context_type, context_key)
);

CREATE INDEX idx_context_session_type ON context(session_id, context_type);
CREATE INDEX idx_context_relevance ON context(relevance_score DESC);
CREATE INDEX idx_context_expires ON context(expires_at) WHERE expires_at IS NOT NULL;

-- State snapshots: Point-in-time state captures
CREATE TABLE state_snapshots (
    id TEXT PRIMARY KEY,
    session_id TEXT REFERENCES sessions(id) ON DELETE CASCADE,
    snapshot_type TEXT CHECK(snapshot_type IN ('checkpoint', 'backup', 'recovery')),
    state_data BLOB,  -- Compressed state
    compression_type TEXT DEFAULT 'zstd',
    checksum TEXT NOT NULL,
    size_bytes INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_snapshots_session ON state_snapshots(session_id, created_at DESC);

-- Decisions table: Decision history and learning
CREATE TABLE decisions (
    id TEXT PRIMARY KEY,
    session_id TEXT REFERENCES sessions(id),
    task_id TEXT REFERENCES tasks(id),
    decision_type TEXT NOT NULL,
    context_hash TEXT NOT NULL,
    decision_made TEXT NOT NULL,
    confidence REAL,
    autonomous BOOLEAN DEFAULT FALSE,
    user_override BOOLEAN DEFAULT FALSE,
    outcome TEXT,
    feedback_score REAL,
    reasoning JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_decisions_context ON decisions(context_hash);
CREATE INDEX idx_decisions_type ON decisions(decision_type);
CREATE INDEX idx_decisions_autonomous ON decisions(autonomous);

-- Preferences table: Learned user preferences
CREATE TABLE user_preferences (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    preference_type TEXT NOT NULL,
    preference_key TEXT NOT NULL,
    preference_value JSONB NOT NULL,
    confidence REAL DEFAULT 0.5,
    observation_count INTEGER DEFAULT 1,
    last_observed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, preference_type, preference_key)
);

CREATE INDEX idx_preferences_user_type ON user_preferences(user_id, preference_type);
CREATE INDEX idx_preferences_confidence ON user_preferences(confidence DESC);
```

### 3.2 Audit and Recovery Tables

```sql
-- Audit log: Complete audit trail
CREATE TABLE audit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_type TEXT NOT NULL,
    entity_type TEXT NOT NULL,
    entity_id TEXT NOT NULL,
    old_value JSONB,
    new_value JSONB,
    change_metadata JSONB,
    user_id TEXT,
    session_id TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_audit_entity ON audit_log(entity_type, entity_id);
CREATE INDEX idx_audit_timestamp ON audit_log(timestamp DESC);

-- Recovery points: System recovery markers
CREATE TABLE recovery_points (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    state_snapshot_id TEXT REFERENCES state_snapshots(id),
    recovery_metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 4. Context Preservation System

### 4.1 Context Engine Implementation

```python
class ContextEngine:
    """Sophisticated context management engine"""

    def __init__(self):
        self.active_contexts = {}
        self.context_graph = ContextGraph()
        self.relevance_calculator = RelevanceCalculator()

    async def capture_context(self, session_id: str, source: str, data: dict) -> Context:
        """Capture and store context from various sources"""

        context = Context(
            session_id=session_id,
            source=source,
            timestamp=datetime.utcnow()
        )

        # Extract context elements
        context.elements = await self.extract_context_elements(data)

        # Calculate relationships
        context.relationships = self.identify_relationships(context.elements)

        # Determine relevance
        context.relevance_score = await self.calculate_relevance(context)

        # Add to context graph
        self.context_graph.add_context(context)

        # Persist
        await self.persist_context(context)

        return context

    async def extract_context_elements(self, data: dict) -> List[ContextElement]:
        """Extract meaningful context elements from data"""

        elements = []

        # File context
        if 'files' in data:
            for file_path in data['files']:
                elements.append(ContextElement(
                    type='file',
                    identifier=file_path,
                    attributes={
                        'path': file_path,
                        'modified': os.path.getmtime(file_path),
                        'size': os.path.getsize(file_path)
                    }
                ))

        # Code context
        if 'code_snippets' in data:
            for snippet in data['code_snippets']:
                elements.append(ContextElement(
                    type='code',
                    identifier=snippet['id'],
                    attributes={
                        'language': snippet['language'],
                        'function': snippet.get('function_name'),
                        'class': snippet.get('class_name'),
                        'imports': snippet.get('imports', [])
                    }
                ))

        # Task context
        if 'task' in data:
            elements.append(ContextElement(
                type='task',
                identifier=data['task']['id'],
                attributes={
                    'description': data['task']['description'],
                    'status': data['task']['status'],
                    'dependencies': data['task'].get('dependencies', [])
                }
            ))

        # Environment context
        if 'environment' in data:
            elements.append(ContextElement(
                type='environment',
                identifier='env',
                attributes={
                    'cwd': os.getcwd(),
                    'python_version': sys.version,
                    'packages': data['environment'].get('packages', {}),
                    'env_vars': self.safe_env_vars()
                }
            ))

        return elements

    async def reconstruct_context(self, session_id: str) -> SessionContext:
        """Reconstruct complete context for session"""

        # Load from cache first
        if cached := await self.load_from_cache(session_id):
            return cached

        # Reconstruct from database
        session_context = SessionContext(session_id=session_id)

        # Load session data
        session_context.session = await self.load_session(session_id)

        # Load active tasks
        session_context.active_tasks = await self.load_active_tasks(session_id)

        # Load recent context
        session_context.recent_context = await self.load_recent_context(session_id)

        # Rebuild context graph
        session_context.context_graph = await self.rebuild_context_graph(session_id)

        # Load user preferences
        session_context.preferences = await self.load_preferences(session_context.session.user_id)

        # Cache reconstructed context
        await self.cache_context(session_context)

        return session_context

    def identify_relationships(self, elements: List[ContextElement]) -> List[ContextRelationship]:
        """Identify relationships between context elements"""

        relationships = []

        for i, elem1 in enumerate(elements):
            for elem2 in elements[i+1:]:
                # File dependencies
                if elem1.type == 'file' and elem2.type == 'file':
                    if self.files_related(elem1, elem2):
                        relationships.append(ContextRelationship(
                            source=elem1.identifier,
                            target=elem2.identifier,
                            type='dependency',
                            strength=0.8
                        ))

                # Code relationships
                if elem1.type == 'code' and elem2.type == 'code':
                    if self.code_related(elem1, elem2):
                        relationships.append(ContextRelationship(
                            source=elem1.identifier,
                            target=elem2.identifier,
                            type='calls',
                            strength=0.9
                        ))

        return relationships
```

### 4.2 Context Relevance Algorithm

```python
class RelevanceCalculator:
    """Calculate context relevance for intelligent retrieval"""

    def __init__(self):
        self.decay_factor = 0.95  # Per hour
        self.access_boost = 0.1
        self.relationship_weight = 0.3

    async def calculate_relevance(self, context: Context) -> float:
        """Calculate relevance score for context"""

        base_score = 1.0

        # Time decay
        age_hours = (datetime.utcnow() - context.timestamp).total_seconds() / 3600
        time_score = base_score * (self.decay_factor ** age_hours)

        # Access frequency boost
        access_score = min(context.access_count * self.access_boost, 0.5)

        # Relationship importance
        relationship_score = 0.0
        if context.relationships:
            avg_strength = sum(r.strength for r in context.relationships) / len(context.relationships)
            relationship_score = avg_strength * self.relationship_weight

        # Task relevance
        task_score = await self.calculate_task_relevance(context)

        # Combined score
        relevance = (time_score * 0.3 +
                    access_score * 0.2 +
                    relationship_score * 0.25 +
                    task_score * 0.25)

        return min(relevance, 1.0)

    async def calculate_task_relevance(self, context: Context) -> float:
        """Calculate relevance to current tasks"""

        # Get active tasks
        active_tasks = await self.get_active_tasks()

        if not active_tasks:
            return 0.5

        relevance_scores = []

        for task in active_tasks:
            score = 0.0

            # Direct task reference
            if context.has_reference(task.id):
                score = 1.0
            # Related file
            elif task.involves_files(context.get_files()):
                score = 0.8
            # Same code area
            elif task.code_area == context.code_area:
                score = 0.6
            # Same project
            elif task.project == context.project:
                score = 0.4

            relevance_scores.append(score)

        return max(relevance_scores) if relevance_scores else 0.0
```

## 5. Memory Management

### 5.1 Hierarchical Memory System

```python
class HierarchicalMemory:
    """Multi-tier memory management system"""

    def __init__(self):
        # Memory tiers
        self.working_memory = WorkingMemory(size_mb=128)  # Hot data
        self.short_term = ShortTermMemory(size_mb=512)    # Warm data
        self.long_term = LongTermMemory()                 # Cold data

        # Memory pressure monitor
        self.pressure_monitor = MemoryPressureMonitor()

        # Eviction policies
        self.eviction_policy = AdaptiveLRU()

    async def store(self, key: str, value: Any, importance: float = 0.5) -> None:
        """Store data in appropriate memory tier"""

        size = sys.getsizeof(value)

        # Determine tier based on importance and size
        if importance > 0.8 and size < 1024 * 1024:  # < 1MB
            await self.working_memory.store(key, value)
        elif importance > 0.5 and size < 10 * 1024 * 1024:  # < 10MB
            await self.short_term.store(key, value)
        else:
            await self.long_term.store(key, value)

        # Check memory pressure
        if self.pressure_monitor.is_high():
            await self.evict_cold_data()

    async def retrieve(self, key: str) -> Optional[Any]:
        """Retrieve data from memory hierarchy"""

        # Check working memory (fastest)
        if value := self.working_memory.get(key):
            return value

        # Check short-term memory
        if value := await self.short_term.get(key):
            # Promote to working memory if frequently accessed
            if self.should_promote(key):
                await self.working_memory.store(key, value)
            return value

        # Check long-term memory (slowest)
        if value := await self.long_term.get(key):
            # Promote based on access pattern
            await self.promote_if_needed(key, value)
            return value

        return None

    async def evict_cold_data(self) -> None:
        """Evict least recently used data"""

        # Get eviction candidates
        candidates = self.eviction_policy.get_candidates(
            self.working_memory.get_all_keys(),
            count=10
        )

        for key in candidates:
            # Move to lower tier instead of deleting
            if value := self.working_memory.get(key):
                await self.short_term.store(key, value)
                self.working_memory.remove(key)

        # Continue with short-term if needed
        if self.pressure_monitor.is_critical():
            st_candidates = self.eviction_policy.get_candidates(
                self.short_term.get_all_keys(),
                count=20
            )

            for key in st_candidates:
                if value := await self.short_term.get(key):
                    await self.long_term.store(key, value)
                    await self.short_term.remove(key)
```

### 5.2 Memory Optimization Strategies

```python
class MemoryOptimizer:
    """Optimize memory usage and access patterns"""

    def __init__(self):
        self.compression = CompressionManager()
        self.deduplication = DeduplicationEngine()
        self.prefetcher = PrefetchEngine()

    async def optimize_storage(self, data: dict) -> dict:
        """Optimize data before storage"""

        # Deduplicate repeated content
        data = await self.deduplication.process(data)

        # Compress large values
        for key, value in data.items():
            if sys.getsizeof(value) > 1024:  # > 1KB
                data[key] = await self.compression.compress(value)

        # Extract and index metadata
        metadata = self.extract_metadata(data)
        data['_metadata'] = metadata

        return data

    async def compress(self, data: Any) -> CompressedData:
        """Compress data for storage"""

        # Serialize to bytes
        serialized = pickle.dumps(data)

        # Choose compression algorithm based on data characteristics
        if len(serialized) < 1024:
            # Small data - use LZ4 for speed
            compressed = lz4.frame.compress(serialized)
            algorithm = 'lz4'
        else:
            # Large data - use zstd for better compression
            compressed = zstd.compress(serialized, level=3)
            algorithm = 'zstd'

        return CompressedData(
            data=compressed,
            algorithm=algorithm,
            original_size=len(serialized),
            compressed_size=len(compressed)
        )

    class DeduplicationEngine:
        """Remove duplicate data across storage"""

        def __init__(self):
            self.hash_index = {}
            self.reference_count = defaultdict(int)

        async def process(self, data: dict) -> dict:
            """Deduplicate data using content hashing"""

            processed = {}

            for key, value in data.items():
                # Calculate content hash
                content_hash = self.calculate_hash(value)

                if content_hash in self.hash_index:
                    # Reference existing data
                    processed[key] = DataReference(content_hash)
                    self.reference_count[content_hash] += 1
                else:
                    # Store new data
                    self.hash_index[content_hash] = value
                    processed[key] = value
                    self.reference_count[content_hash] = 1

            return processed

        def calculate_hash(self, data: Any) -> str:
            """Calculate stable hash for data"""

            # Convert to bytes
            if isinstance(data, bytes):
                content = data
            else:
                content = json.dumps(data, sort_keys=True).encode()

            # Use SHA256 for content addressing
            return hashlib.sha256(content).hexdigest()
```

## 6. State Synchronization

### 6.1 Synchronization Manager

```python
class SyncManager:
    """Manage state synchronization across components"""

    def __init__(self):
        self.sync_queue = asyncio.Queue()
        self.sync_status = {}
        self.conflict_resolver = ConflictResolver()
        self.version_tracker = VersionTracker()

    async def sync_state(self, component: str, state: dict) -> SyncResult:
        """Synchronize state from component"""

        # Create sync request
        request = SyncRequest(
            component=component,
            state=state,
            version=self.version_tracker.get_version(component),
            timestamp=datetime.utcnow()
        )

        # Check for conflicts
        if conflicts := await self.detect_conflicts(request):
            resolved_state = await self.conflict_resolver.resolve(conflicts, request)
            request.state = resolved_state

        # Apply state update
        result = await self.apply_state_update(request)

        # Update version
        self.version_tracker.increment(component)

        # Propagate to other components
        await self.propagate_state_change(component, result.state)

        return result

    async def detect_conflicts(self, request: SyncRequest) -> List[Conflict]:
        """Detect conflicts with current state"""

        conflicts = []
        current_state = await self.get_current_state(request.component)

        for key, new_value in request.state.items():
            if key in current_state:
                old_value = current_state[key]

                # Check if values differ
                if old_value != new_value:
                    # Check timestamps
                    if self.is_concurrent_modification(key, request.timestamp):
                        conflicts.append(Conflict(
                            key=key,
                            old_value=old_value,
                            new_value=new_value,
                            type='concurrent_modification'
                        ))

        return conflicts

    async def propagate_state_change(self, source: str, state: dict) -> None:
        """Propagate state changes to interested components"""

        # Get subscribed components
        subscribers = self.get_subscribers(source)

        # Create propagation tasks
        tasks = []
        for subscriber in subscribers:
            if subscriber != source:  # Don't propagate back to source
                tasks.append(self.notify_component(subscriber, state))

        # Execute notifications in parallel
        await asyncio.gather(*tasks, return_exceptions=True)
```

### 6.2 Conflict Resolution

```python
class ConflictResolver:
    """Resolve state conflicts intelligently"""

    def __init__(self):
        self.resolution_strategies = {
            'last_write_wins': self.last_write_wins,
            'merge': self.merge_states,
            'user_decides': self.escalate_to_user,
            'rule_based': self.apply_rules
        }

    async def resolve(self, conflicts: List[Conflict], request: SyncRequest) -> dict:
        """Resolve conflicts based on type and context"""

        resolved_state = request.state.copy()

        for conflict in conflicts:
            # Determine resolution strategy
            strategy = self.select_strategy(conflict)

            # Apply resolution
            resolved_value = await self.resolution_strategies[strategy](conflict)

            # Update state
            resolved_state[conflict.key] = resolved_value

            # Log resolution
            await self.log_resolution(conflict, strategy, resolved_value)

        return resolved_state

    def select_strategy(self, conflict: Conflict) -> str:
        """Select appropriate resolution strategy"""

        # Critical conflicts need user decision
        if self.is_critical(conflict):
            return 'user_decides'

        # Mergeable data structures
        if self.is_mergeable(conflict):
            return 'merge'

        # Apply rules for known patterns
        if self.has_resolution_rule(conflict):
            return 'rule_based'

        # Default to last write wins
        return 'last_write_wins'

    async def merge_states(self, conflict: Conflict) -> Any:
        """Merge conflicting states intelligently"""

        old_value = conflict.old_value
        new_value = conflict.new_value

        # List merge - combine unique elements
        if isinstance(old_value, list) and isinstance(new_value, list):
            merged = list(set(old_value + new_value))
            return merged

        # Dict merge - recursive merge
        if isinstance(old_value, dict) and isinstance(new_value, dict):
            merged = old_value.copy()
            for key, value in new_value.items():
                if key in merged and isinstance(merged[key], dict):
                    merged[key] = await self.merge_states(Conflict(
                        key=key,
                        old_value=merged[key],
                        new_value=value
                    ))
                else:
                    merged[key] = value
            return merged

        # Set merge - union
        if isinstance(old_value, set) and isinstance(new_value, set):
            return old_value | new_value

        # Default to new value if types don't match
        return new_value
```

## 7. Recovery Mechanisms

### 7.1 Recovery Manager

```python
class RecoveryManager:
    """Handle state recovery and restoration"""

    def __init__(self):
        self.recovery_points = []
        self.recovery_strategies = {
            'full': self.full_recovery,
            'incremental': self.incremental_recovery,
            'selective': self.selective_recovery
        }

    async def create_recovery_point(self, name: str = None) -> RecoveryPoint:
        """Create a recovery point"""

        # Generate snapshot
        snapshot = await self.create_snapshot()

        # Create recovery point
        recovery_point = RecoveryPoint(
            id=generate_uuid(),
            name=name or f"auto_{datetime.utcnow().isoformat()}",
            snapshot_id=snapshot.id,
            timestamp=datetime.utcnow(),
            metadata={
                'active_tasks': await self.get_active_task_count(),
                'session_count': await self.get_session_count(),
                'state_size': snapshot.size_bytes
            }
        )

        # Store recovery point
        await self.store_recovery_point(recovery_point)
        self.recovery_points.append(recovery_point)

        return recovery_point

    async def recover(self, recovery_point_id: str, strategy: str = 'full') -> RecoveryResult:
        """Recover to a specific point"""

        # Load recovery point
        recovery_point = await self.load_recovery_point(recovery_point_id)

        if not recovery_point:
            raise RecoveryError(f"Recovery point {recovery_point_id} not found")

        # Execute recovery strategy
        recovery_func = self.recovery_strategies[strategy]
        result = await recovery_func(recovery_point)

        # Verify recovery
        if not await self.verify_recovery(result):
            await self.rollback_recovery(result)
            raise RecoveryError("Recovery verification failed")

        # Log recovery
        await self.log_recovery(recovery_point, result)

        return result

    async def full_recovery(self, recovery_point: RecoveryPoint) -> RecoveryResult:
        """Full state recovery from snapshot"""

        result = RecoveryResult()

        try:
            # Load snapshot
            snapshot = await self.load_snapshot(recovery_point.snapshot_id)

            # Decompress state
            state_data = await self.decompress_snapshot(snapshot)

            # Clear current state
            await self.clear_current_state()

            # Restore state
            await self.restore_state(state_data)

            # Restore active sessions
            await self.restore_sessions(state_data['sessions'])

            # Restore context
            await self.restore_context(state_data['context'])

            result.success = True
            result.recovered_items = len(state_data.get('tasks', []))

        except Exception as e:
            result.success = False
            result.error = str(e)
            self.logger.error(f"Recovery failed: {e}")

        return result

    async def verify_recovery(self, result: RecoveryResult) -> bool:
        """Verify recovery was successful"""

        checks = [
            self.verify_database_integrity(),
            self.verify_state_consistency(),
            self.verify_context_relationships(),
            self.verify_task_dependencies()
        ]

        results = await asyncio.gather(*checks, return_exceptions=True)

        for check_result in results:
            if isinstance(check_result, Exception):
                self.logger.error(f"Verification failed: {check_result}")
                return False
            if not check_result:
                return False

        return True
```

### 7.2 Automatic Recovery Detection

```python
class AutoRecovery:
    """Automatic corruption detection and recovery"""

    def __init__(self):
        self.integrity_checker = IntegrityChecker()
        self.corruption_detector = CorruptionDetector()
        self.auto_repair = AutoRepair()

    async def monitor_health(self) -> None:
        """Continuously monitor state health"""

        while True:
            try:
                # Check integrity
                if issues := await self.integrity_checker.check():
                    await self.handle_integrity_issues(issues)

                # Check for corruption
                if corruption := await self.corruption_detector.scan():
                    await self.handle_corruption(corruption)

                # Check consistency
                if inconsistencies := await self.check_consistency():
                    await self.handle_inconsistencies(inconsistencies)

            except Exception as e:
                self.logger.error(f"Health monitor error: {e}")

            # Sleep before next check
            await asyncio.sleep(60)  # Check every minute

    async def handle_corruption(self, corruption: List[CorruptedItem]) -> None:
        """Handle detected corruption"""

        for item in corruption:
            self.logger.warning(f"Corruption detected in {item.type}: {item.id}")

            # Attempt auto-repair
            if await self.auto_repair.can_repair(item):
                if await self.auto_repair.repair(item):
                    self.logger.info(f"Successfully repaired {item.id}")
                else:
                    # Escalate if auto-repair fails
                    await self.escalate_corruption(item)
            else:
                # Use recovery point if available
                if recovery_point := await self.find_recovery_point(item):
                    await self.selective_recovery(item, recovery_point)
                else:
                    await self.escalate_corruption(item)
```

## 8. Query Optimization

### 8.1 Query Optimizer

```python
class QueryOptimizer:
    """Optimize state queries for performance"""

    def __init__(self):
        self.query_cache = QueryCache(size_mb=128)
        self.index_manager = IndexManager()
        self.statistics = QueryStatistics()
        self.query_planner = QueryPlanner()

    async def optimize_query(self, query: StateQuery) -> OptimizedQuery:
        """Optimize query for execution"""

        # Check cache first
        cache_key = self.generate_cache_key(query)
        if cached := self.query_cache.get(cache_key):
            self.statistics.record_cache_hit()
            return cached

        # Analyze query
        analysis = await self.analyze_query(query)

        # Generate query plan
        plan = await self.query_planner.create_plan(query, analysis)

        # Optimize based on statistics
        if self.statistics.is_frequent_query(query):
            plan = await self.optimize_for_frequency(plan)

        # Create indexes if beneficial
        if self.should_create_index(analysis):
            await self.index_manager.create_index(analysis.suggested_index)

        # Build optimized query
        optimized = OptimizedQuery(
            original=query,
            plan=plan,
            estimated_cost=plan.estimated_cost,
            use_cache=analysis.cacheable
        )

        # Cache if appropriate
        if analysis.cacheable:
            self.query_cache.set(cache_key, optimized)

        return optimized

    async def analyze_query(self, query: StateQuery) -> QueryAnalysis:
        """Analyze query for optimization opportunities"""

        analysis = QueryAnalysis()

        # Identify query type
        analysis.type = self.identify_query_type(query)

        # Estimate selectivity
        analysis.selectivity = await self.estimate_selectivity(query)

        # Check for index usage
        analysis.uses_index = await self.check_index_usage(query)

        # Suggest optimizations
        if analysis.selectivity < 0.1 and not analysis.uses_index:
            analysis.suggested_index = self.suggest_index(query)

        # Determine if cacheable
        analysis.cacheable = (
            query.is_deterministic and
            not query.includes_current_time and
            analysis.selectivity < 0.2
        )

        return analysis

    class QueryPlanner:
        """Create optimal query execution plans"""

        async def create_plan(self, query: StateQuery, analysis: QueryAnalysis) -> QueryPlan:
            """Generate query execution plan"""

            plan = QueryPlan()

            # Determine access path
            if analysis.uses_index:
                plan.access_method = 'index_scan'
                plan.index_name = analysis.index_used
            else:
                plan.access_method = 'full_scan'

            # Optimize join order if needed
            if query.has_joins():
                plan.join_order = await self.optimize_join_order(query)

            # Add filtering strategy
            plan.filter_strategy = self.select_filter_strategy(query, analysis)

            # Estimate cost
            plan.estimated_cost = await self.estimate_cost(plan, analysis)

            # Add parallelization if beneficial
            if plan.estimated_cost > 100 and query.allows_parallel():
                plan.parallel_degree = self.calculate_parallel_degree(plan)

            return plan
```

### 8.2 Index Management

```python
class IndexManager:
    """Manage database indexes for optimal performance"""

    def __init__(self):
        self.indexes = {}
        self.usage_stats = defaultdict(int)
        self.maintenance_scheduler = MaintenanceScheduler()

    async def create_index(self, index_spec: IndexSpecification) -> None:
        """Create new index"""

        # Validate index doesn't exist
        if self.index_exists(index_spec):
            return

        # Generate index name
        index_name = self.generate_index_name(index_spec)

        # Create index SQL
        sql = f"""
        CREATE INDEX {index_name}
        ON {index_spec.table}({', '.join(index_spec.columns)})
        """

        if index_spec.where_clause:
            sql += f" WHERE {index_spec.where_clause}"

        # Execute index creation
        await self.execute_ddl(sql)

        # Register index
        self.indexes[index_name] = index_spec

        # Schedule maintenance
        self.maintenance_scheduler.schedule_reindex(index_name)

    async def analyze_index_usage(self) -> IndexUsageReport:
        """Analyze index usage patterns"""

        report = IndexUsageReport()

        # Get index statistics
        for index_name, spec in self.indexes.items():
            stats = await self.get_index_statistics(index_name)

            usage = IndexUsage(
                name=index_name,
                table=spec.table,
                columns=spec.columns,
                size_bytes=stats['size'],
                scan_count=stats['scan_count'],
                tuple_read=stats['tuple_read'],
                efficiency=stats['tuple_read'] / max(stats['scan_count'], 1)
            )

            report.index_usage.append(usage)

        # Identify unused indexes
        report.unused_indexes = [
            usage.name for usage in report.index_usage
            if usage.scan_count == 0
        ]

        # Identify inefficient indexes
        report.inefficient_indexes = [
            usage.name for usage in report.index_usage
            if usage.efficiency < 0.1 and usage.scan_count > 100
        ]

        # Suggest new indexes
        report.suggested_indexes = await self.suggest_new_indexes()

        return report
```

## 9. Garbage Collection

### 9.1 Garbage Collector Implementation

```python
class GarbageCollector:
    """Intelligent garbage collection for state management"""

    def __init__(self):
        self.collection_policy = CollectionPolicy()
        self.retention_rules = RetentionRules()
        self.collection_stats = CollectionStatistics()

    async def collect(self, force: bool = False) -> CollectionResult:
        """Perform garbage collection"""

        result = CollectionResult()

        # Check if collection needed
        if not force and not self.should_collect():
            result.skipped = True
            return result

        # Phase 1: Mark
        marked = await self.mark_phase()

        # Phase 2: Sweep
        swept = await self.sweep_phase(marked)

        # Phase 3: Compact
        if self.should_compact():
            await self.compact_phase()

        # Update statistics
        result.items_marked = len(marked)
        result.items_collected = swept
        result.space_reclaimed = await self.calculate_reclaimed_space()

        self.collection_stats.record(result)

        return result

    async def mark_phase(self) -> Set[str]:
        """Mark reachable objects"""

        reachable = set()
        roots = await self.get_gc_roots()

        # Traverse from roots
        queue = list(roots)
        visited = set()

        while queue:
            item_id = queue.pop(0)

            if item_id in visited:
                continue

            visited.add(item_id)
            reachable.add(item_id)

            # Find references
            references = await self.get_references(item_id)
            queue.extend(ref for ref in references if ref not in visited)

        return reachable

    async def sweep_phase(self, marked: Set[str]) -> int:
        """Remove unreachable objects"""

        all_objects = await self.get_all_object_ids()
        unreachable = all_objects - marked
        collected_count = 0

        for obj_id in unreachable:
            # Check retention rules
            if await self.should_retain(obj_id):
                continue

            # Collect object
            await self.collect_object(obj_id)
            collected_count += 1

        return collected_count

    async def should_retain(self, obj_id: str) -> bool:
        """Check if object should be retained despite being unreachable"""

        obj = await self.get_object_metadata(obj_id)

        # Check retention rules
        for rule in self.retention_rules.rules:
            if rule.matches(obj):
                if rule.should_retain(obj):
                    return True

        # Check age-based retention
        age = datetime.utcnow() - obj.created_at
        if age < timedelta(hours=24):  # Keep recent objects
            return True

        # Check importance
        if obj.importance > 0.8:
            return True

        return False

    class RetentionRules:
        """Define retention policies"""

        def __init__(self):
            self.rules = [
                RetentionRule(
                    name="active_session",
                    condition="obj.type == 'session' and obj.status == 'active'",
                    retain=True,
                    priority=100
                ),
                RetentionRule(
                    name="recent_decision",
                    condition="obj.type == 'decision' and obj.age_hours < 72",
                    retain=True,
                    priority=90
                ),
                RetentionRule(
                    name="user_preference",
                    condition="obj.type == 'preference'",
                    retain=True,
                    priority=95
                ),
                RetentionRule(
                    name="checkpoint",
                    condition="obj.type == 'checkpoint' and obj.is_recovery_point",
                    retain=True,
                    priority=100
                )
            ]
```

## 10. Performance Metrics

### 10.1 Performance Monitoring

```python
class StatePerformanceMonitor:
    """Monitor state system performance"""

    def __init__(self):
        self.metrics = {
            'query_latency': Histogram('state_query_latency_seconds'),
            'write_latency': Histogram('state_write_latency_seconds'),
            'cache_hit_rate': Gauge('state_cache_hit_rate'),
            'memory_usage': Gauge('state_memory_usage_bytes'),
            'gc_duration': Histogram('state_gc_duration_seconds'),
            'recovery_time': Histogram('state_recovery_time_seconds')
        }

    async def record_operation(self, operation: str, duration: float) -> None:
        """Record operation metrics"""

        if operation == 'query':
            self.metrics['query_latency'].observe(duration)
        elif operation == 'write':
            self.metrics['write_latency'].observe(duration)

        # Update cache hit rate
        hit_rate = await self.calculate_cache_hit_rate()
        self.metrics['cache_hit_rate'].set(hit_rate)

        # Update memory usage
        memory = await self.get_memory_usage()
        self.metrics['memory_usage'].set(memory)

    async def generate_performance_report(self) -> PerformanceReport:
        """Generate comprehensive performance report"""

        report = PerformanceReport()

        # Query performance
        report.avg_query_latency = await self.get_metric_average('query_latency')
        report.p95_query_latency = await self.get_metric_percentile('query_latency', 95)

        # Write performance
        report.avg_write_latency = await self.get_metric_average('write_latency')
        report.write_throughput = await self.calculate_write_throughput()

        # Cache effectiveness
        report.cache_hit_rate = self.metrics['cache_hit_rate'].get()
        report.cache_size_mb = await self.get_cache_size() / (1024 * 1024)

        # Memory usage
        report.memory_usage_mb = self.metrics['memory_usage'].get() / (1024 * 1024)
        report.memory_efficiency = await self.calculate_memory_efficiency()

        # GC impact
        report.gc_frequency = await self.calculate_gc_frequency()
        report.avg_gc_duration = await self.get_metric_average('gc_duration')

        return report
```

## 11. State Migration

### 11.1 Migration System

```python
class StateMigrationSystem:
    """Handle state schema and format migrations"""

    def __init__(self):
        self.migration_registry = MigrationRegistry()
        self.version_manager = StateVersionManager()

    async def migrate(self, from_version: str, to_version: str) -> MigrationResult:
        """Perform state migration"""

        result = MigrationResult()

        # Get migration path
        path = self.migration_registry.get_path(from_version, to_version)

        if not path:
            raise MigrationError(f"No migration path from {from_version} to {to_version}")

        # Create backup before migration
        backup = await self.create_pre_migration_backup()
        result.backup_id = backup.id

        # Execute migrations in sequence
        for migration in path:
            try:
                await self.execute_migration(migration)
                result.completed_migrations.append(migration.name)
            except Exception as e:
                result.failed_migration = migration.name
                result.error = str(e)

                # Rollback on failure
                await self.rollback_migration(backup)
                raise

        # Update version
        await self.version_manager.update_version(to_version)
        result.success = True

        return result

    async def execute_migration(self, migration: Migration) -> None:
        """Execute single migration"""

        self.logger.info(f"Executing migration: {migration.name}")

        # Pre-migration checks
        await migration.pre_check()

        # Execute migration
        await migration.execute()

        # Post-migration validation
        await migration.validate()

        self.logger.info(f"Migration {migration.name} completed successfully")
```

## 12. Summary

The State & Context System provides a robust foundation for persistent, intelligent state management:

1. **Multi-tier Storage**: Hot/warm/cold storage with intelligent data placement
2. **Context Preservation**: Complete context capture and reconstruction across sessions
3. **Memory Optimization**: Compression, deduplication, and adaptive eviction
4. **Synchronization**: Conflict detection and resolution for consistent state
5. **Recovery**: Automatic corruption detection and recovery mechanisms
6. **Performance**: Query optimization and intelligent caching
7. **Garbage Collection**: Smart cleanup while preserving important data

This design ensures the system can maintain complete context across multi-day work sessions while optimizing for performance and reliability.