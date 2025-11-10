"""
Conversation archiver.

Archives main session and subagent conversation logs with metadata.
"""

import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional
try:
    from .common import (
        LOGS_DIR,
        log_error,
        save_json,
        load_json,
        get_month_dir,
        format_timestamp,
        ensure_permissions
    )
    from .sanitizer import sanitize_content
except ImportError:
    from common import (
        LOGS_DIR,
        log_error,
        save_json,
        load_json,
        get_month_dir,
        format_timestamp,
        ensure_permissions
    )
    from sanitizer import sanitize_content


class ConversationArchiver:
    """Archive conversation transcripts with metadata and indexing."""

    def __init__(self, archive_type: str = "main-session"):
        """
        Initialize archiver.

        Args:
            archive_type: "main-session" or "subagent/{agent_type}"
        """
        self.archive_type = archive_type
        self.base_dir = LOGS_DIR / archive_type
        self.base_dir.mkdir(parents=True, exist_ok=True)
        ensure_permissions(self.base_dir, is_dir=True)

    def archive_session(
        self,
        session_id: str,
        transcript_path: str,
        metadata: Dict,
        sanitize: bool = False
    ):
        """
        Archive a conversation session.

        Args:
            session_id: Session identifier
            transcript_path: Path to transcript file
            metadata: Session metadata
            sanitize: Whether to sanitize sensitive data
        """
        try:
            # Create month directory
            month_dir = self.base_dir / get_month_dir()
            month_dir.mkdir(parents=True, exist_ok=True)
            ensure_permissions(month_dir, is_dir=True)

            # Generate filename
            timestamp = format_timestamp()
            base_name = f"{timestamp}_{session_id}"

            # Copy transcript
            transcript_src = Path(transcript_path)
            if not transcript_src.exists():
                log_error(f"Transcript not found: {transcript_path}", level="WARNING")
                return

            transcript_dst = month_dir / f"{base_name}.jsonl"

            if sanitize:
                self._copy_and_sanitize(transcript_src, transcript_dst)
            else:
                shutil.copy2(transcript_src, transcript_dst)

            ensure_permissions(transcript_dst)

            # Save metadata
            meta_path = month_dir / f"{base_name}.meta.json"
            metadata.update({
                "archive_path": str(transcript_dst.relative_to(LOGS_DIR)),
                "archived_at": datetime.now().isoformat(),
                "sanitized": sanitize,
                "session_id": session_id
            })
            save_json(meta_path, metadata)
            ensure_permissions(meta_path)

            log_error(
                f"Archived session {session_id} to {transcript_dst.relative_to(LOGS_DIR)}",
                level="INFO"
            )

        except Exception as e:
            log_error(f"Failed to archive session {session_id}: {e}")

    def generate_metadata(
        self,
        session_id: str,
        transcript_path: str,
        additional_meta: Optional[Dict] = None
    ) -> Dict:
        """
        Generate metadata for a session.

        Args:
            session_id: Session identifier
            transcript_path: Path to transcript file
            additional_meta: Additional metadata to include

        Returns:
            Metadata dictionary
        """
        metadata = {
            "schema_version": "1.0",
            "session_id": session_id,
            "type": self.archive_type,
            "archived_at": datetime.now().isoformat()
        }

        # Add additional metadata
        if additional_meta:
            metadata.update(additional_meta)

        # Parse transcript for statistics
        try:
            transcript = Path(transcript_path)
            if transcript.exists():
                stats = self._analyze_transcript(transcript)
                metadata.update(stats)

        except Exception as e:
            log_error(f"Error generating metadata for {session_id}: {e}")

        return metadata

    def _analyze_transcript(self, transcript_path: Path) -> Dict:
        """
        Analyze transcript file for statistics.

        Args:
            transcript_path: Path to transcript file

        Returns:
            Statistics dictionary
        """
        stats = {
            "message_count": 0,
            "size_bytes": 0,
            "tool_calls": 0,
            "skills_used": [],
            "files_modified": []
        }

        try:
            stats["size_bytes"] = transcript_path.stat().st_size

            with open(transcript_path, 'r') as f:
                for line in f:
                    stats["message_count"] += 1

                    try:
                        import json
                        data = json.loads(line.strip())

                        # Count tool calls
                        if "tool_name" in data or "tool_calls" in data:
                            stats["tool_calls"] += 1

                        # Track skills
                        if data.get("tool_name") == "Skill":
                            skill_name = data.get("tool_input", {}).get("skill_name")
                            if skill_name and skill_name not in stats["skills_used"]:
                                stats["skills_used"].append(skill_name)

                        # Track file modifications
                        if data.get("tool_name") in ["Write", "Edit"]:
                            file_path = data.get("tool_input", {}).get("file_path")
                            if file_path and file_path not in stats["files_modified"]:
                                stats["files_modified"].append(file_path)

                    except json.JSONDecodeError:
                        # Skip malformed lines
                        pass

        except Exception as e:
            log_error(f"Error analyzing transcript {transcript_path}: {e}")

        return stats

    def _copy_and_sanitize(self, src: Path, dst: Path):
        """
        Copy transcript file with sanitization.

        Args:
            src: Source file path
            dst: Destination file path
        """
        try:
            with open(src, 'r') as f_in, open(dst, 'w') as f_out:
                for line in f_in:
                    sanitized_line = sanitize_content(line)
                    f_out.write(sanitized_line)

        except Exception as e:
            log_error(f"Error sanitizing {src}: {e}")
            # Fallback to regular copy
            shutil.copy2(src, dst)

    def update_index(self, metadata: Dict):
        """
        Update archive index with new session.

        Args:
            metadata: Session metadata
        """
        try:
            index_path = self.base_dir / 'index.json'

            # Load existing index
            index = load_json(index_path, default={
                "schema_version": "1.0",
                "last_updated": "",
                "sessions": [],
                "by_date": {},
                "by_month": {},
                "total_sessions": 0,
                "total_size_bytes": 0
            })

            # Add session
            session_entry = {
                "session_id": metadata["session_id"],
                "timestamp": metadata["archived_at"],
                "archive_path": metadata["archive_path"],
                "message_count": metadata.get("message_count", 0),
                "size_bytes": metadata.get("size_bytes", 0)
            }

            index["sessions"].append(session_entry)
            index["total_sessions"] += 1
            index["total_size_bytes"] += metadata.get("size_bytes", 0)

            # Index by date
            date = metadata["archived_at"][:10]  # YYYY-MM-DD
            if date not in index["by_date"]:
                index["by_date"][date] = []
            index["by_date"][date].append(metadata["session_id"])

            # Index by month
            month = metadata["archived_at"][:7]  # YYYY-MM
            if month not in index["by_month"]:
                index["by_month"][month] = 0
            index["by_month"][month] += 1

            # Update timestamp
            index["last_updated"] = datetime.now().isoformat()

            # Save index
            save_json(index_path, index)
            ensure_permissions(index_path)

        except Exception as e:
            log_error(f"Failed to update index: {e}")
