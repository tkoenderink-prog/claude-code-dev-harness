"""
Skill usage tracker.

Tracks Skill tool invocations with:
- Aggregate counts per skill
- Full invocation history
- Session correlation
- Success rate tracking
- Performance metrics
"""

from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
try:
    from .common import (
        LOGS_DIR,
        file_lock,
        log_error,
        load_json,
        save_json,
        ensure_permissions
    )
except ImportError:
    from common import (
        LOGS_DIR,
        file_lock,
        log_error,
        load_json,
        save_json,
        ensure_permissions
    )

SKILL_USAGE_FILE = LOGS_DIR / 'skill-usage.json'
MAX_INVOCATIONS = 100  # Keep last N invocations per skill
BATCH_SIZE = 10  # Flush after N invocations


class SkillTracker:
    """Track skill invocations with batching for performance."""

    def __init__(self):
        """Initialize tracker with empty batch."""
        self.batch: List[tuple] = []
        self.batch_size = BATCH_SIZE

    def track(
        self,
        skill_name: str,
        session_id: str,
        context: str = "",
        success: bool = True,
        duration_ms: Optional[int] = None
    ):
        """
        Track a skill invocation.

        Args:
            skill_name: Name of skill invoked
            session_id: Session identifier
            context: Execution context/reason
            success: Whether execution succeeded
            duration_ms: Execution duration in milliseconds
        """
        invocation = {
            "timestamp": datetime.now().isoformat(),
            "session_id": session_id,
            "context": context,
            "success": success
        }

        if duration_ms is not None:
            invocation["duration_ms"] = duration_ms

        self.batch.append((skill_name, invocation))

        # Auto-flush if batch size reached
        if len(self.batch) >= self.batch_size:
            self.flush()

    def flush(self):
        """Flush batch to disk with file locking."""
        if not self.batch:
            return

        try:
            with file_lock(SKILL_USAGE_FILE):
                usage = self._load_usage()

                # Process batch
                for skill_name, invocation in self.batch:
                    self._update_usage(usage, skill_name, invocation)

                # Update metadata
                usage["last_updated"] = datetime.now().isoformat()

                # Save
                save_json(SKILL_USAGE_FILE, usage)
                ensure_permissions(SKILL_USAGE_FILE)

            # Clear batch
            self.batch = []

        except Exception as e:
            log_error(f"Failed to flush skill tracking batch: {e}")
            # Don't raise - graceful degradation

    def _load_usage(self) -> Dict:
        """Load skill usage data with default structure."""
        default = {
            "schema_version": "1.0",
            "last_updated": "",
            "total_invocations": 0,
            "skills": {},
            "sessions": {},
            "daily_stats": {}
        }

        return load_json(SKILL_USAGE_FILE, default=default)

    def _update_usage(self, usage: Dict, skill_name: str, invocation: Dict):
        """
        Update usage data with new invocation.

        Args:
            usage: Usage data dictionary
            skill_name: Name of skill
            invocation: Invocation record
        """
        # Initialize skill if new
        if skill_name not in usage["skills"]:
            usage["skills"][skill_name] = {
                "count": 0,
                "first_used": invocation["timestamp"],
                "last_used": invocation["timestamp"],
                "invocations": [],
                "sessions": [],
                "success_count": 0,
                "failure_count": 0,
                "total_duration_ms": 0
            }

        skill = usage["skills"][skill_name]

        # Update counts
        skill["count"] += 1
        skill["last_used"] = invocation["timestamp"]

        if invocation.get("success", True):
            skill["success_count"] += 1
        else:
            skill["failure_count"] += 1

        # Update duration
        if "duration_ms" in invocation:
            skill["total_duration_ms"] += invocation["duration_ms"]

        # Keep last MAX_INVOCATIONS invocations
        skill["invocations"].append(invocation)
        if len(skill["invocations"]) > MAX_INVOCATIONS:
            skill["invocations"] = skill["invocations"][-MAX_INVOCATIONS:]

        # Track unique sessions
        session_id = invocation["session_id"]
        if session_id not in skill["sessions"]:
            skill["sessions"].append(session_id)

        # Update total invocations
        usage["total_invocations"] += 1

        # Update session stats
        self._update_session_stats(usage, skill_name, session_id, invocation)

        # Update daily stats
        self._update_daily_stats(usage, skill_name, session_id, invocation)

        # Calculate derived metrics
        self._calculate_metrics(skill)

    def _update_session_stats(
        self,
        usage: Dict,
        skill_name: str,
        session_id: str,
        invocation: Dict
    ):
        """Update per-session statistics."""
        if session_id not in usage["sessions"]:
            usage["sessions"][session_id] = {
                "started": invocation["timestamp"],
                "skills_used": [],
                "total_invocations": 0
            }

        session = usage["sessions"][session_id]
        session["total_invocations"] += 1

        if skill_name not in session["skills_used"]:
            session["skills_used"].append(skill_name)

    def _update_daily_stats(
        self,
        usage: Dict,
        skill_name: str,
        session_id: str,
        invocation: Dict
    ):
        """Update daily statistics."""
        date = invocation["timestamp"][:10]  # YYYY-MM-DD

        if date not in usage["daily_stats"]:
            usage["daily_stats"][date] = {
                "invocations": 0,
                "unique_skills": [],
                "unique_sessions": []
            }

        stats = usage["daily_stats"][date]
        stats["invocations"] += 1

        if skill_name not in stats["unique_skills"]:
            stats["unique_skills"].append(skill_name)

        if session_id not in stats["unique_sessions"]:
            stats["unique_sessions"].append(session_id)

    def _calculate_metrics(self, skill: Dict):
        """Calculate derived metrics for a skill."""
        # Success rate
        total = skill["success_count"] + skill["failure_count"]
        if total > 0:
            skill["success_rate"] = skill["success_count"] / total
        else:
            skill["success_rate"] = 1.0

        # Average duration
        if skill["count"] > 0 and skill["total_duration_ms"] > 0:
            skill["avg_duration_ms"] = skill["total_duration_ms"] / skill["count"]
        else:
            skill["avg_duration_ms"] = 0


def track_skill_usage(
    skill_name: str,
    session_id: str,
    context: str = "",
    success: bool = True,
    duration_ms: Optional[int] = None
):
    """
    Convenience function to track a single skill invocation.

    Args:
        skill_name: Name of skill invoked
        session_id: Session identifier
        context: Execution context/reason
        success: Whether execution succeeded
        duration_ms: Execution duration in milliseconds
    """
    tracker = SkillTracker()
    tracker.track(skill_name, session_id, context, success, duration_ms)
    tracker.flush()  # Immediate flush for single invocation
