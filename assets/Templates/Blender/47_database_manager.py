#!/usr/bin/env python3
"""
TASK COMPLETION DATABASE MANAGER
This script manages the comprehensive task tracking database
to ensure EVERY task is completed fully and nothing is left undone.
"""

import sqlite3
import json
import os
import re
from datetime import datetime
from typing import List, Dict, Any, Optional
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Database Storage Strategy Configuration
DATABASE_STORAGE_CONFIG = {
    "local_databases": {
        # Performance-critical databases that MUST remain local for video/avatar creation
        "performance_critical": [
            "content_automation.db",
            "quality_metrics.db",
            "performance_metrics.db",
            "automation_performance.db",
            "runtime.db",
            "model_generator.db",
            "ollama_cache.db",
        ],
        "description": "Databases required for high-speed video creation and avatar generation",
    },
    "cloud_databases": {
        # Databases that can be moved to cloud storage
        "analytics": [
            "analytics_dashboard.db",
            "analytics.db",
            "performance_analytics.db",
            "engagement_tracking.sqlite",
            "youtube_engagement.sqlite",
        ],
        "business": [
            "marketing_monetization.sqlite",
            "marketing.db",
            "monetization.db",
            "revenue_streams.db",
            "cost_tracking.db",
            "promotion_campaigns.sqlite",
        ],
        "content_management": [
            "rss_watcher.db",
            "youtube_automation.sqlite",
            "channels.db",
            "collaboration_outreach.db",
        ],
        "system_admin": [
            "error_tracking.db",
            "example_error_tracking.db",
            "scan_results.sqlite",
            "api_integration.db",
            "routellm_usage.db",
        ],
        "development": [
            "test_comprehensive.db",
            "test_fraud.db",
            "test_fraud2.db",
            "test_fraud3.db",
            "test_results.db",
            "test.db",
        ],
        "backups": [
            "right_perspective_backup_20250902_012246.db",
            "base44.sqlite",
            "trae_production.db",
        ],
        "description": "Databases suitable for cloud storage - non-performance critical",
    },
    "hybrid_databases": {
        # Databases that may need evaluation based on usage patterns
        "evaluate_case_by_case": [
            "intelligence.db",
            "master_orchestrator.db",
            "trae_ai.db",
            "content_agent.db",
        ],
        "description": "Databases requiring evaluation based on access patterns and usage frequency",
    },
}


class DatabaseStorageManager:
    """Manages database storage strategy for local vs cloud deployment"""

    def __init__(self):
        self.config = DATABASE_STORAGE_CONFIG

    def is_performance_critical(self, db_name: str) -> bool:
        """Check if database must remain local for performance"""
        return db_name in self.config["local_databases"]["performance_critical"]

    def can_move_to_cloud(self, db_name: str) -> bool:
        """Check if database can be moved to cloud storage"""
        for category in self.config["cloud_databases"].values():
            if isinstance(category, list) and db_name in category:
                return True
        return False

    def requires_evaluation(self, db_name: str) -> bool:
        """Check if database requires case-by-case evaluation"""
        return db_name in self.config["hybrid_databases"]["evaluate_case_by_case"]

    def get_storage_recommendation(self, db_name: str) -> Dict[str, str]:
        """Get storage recommendation for a database"""
        if self.is_performance_critical(db_name):
            return {
                "recommendation": "local",
                "reason": "Performance-critical for video/avatar creation",
                "category": "performance_critical",
            }
        elif self.can_move_to_cloud(db_name):
            return {
                "recommendation": "cloud",
                "reason": "Non-performance critical, suitable for cloud storage",
                "category": self._get_cloud_category(db_name),
            }
        elif self.requires_evaluation(db_name):
            return {
                "recommendation": "evaluate",
                "reason": "Requires case-by-case evaluation based on usage patterns",
                "category": "hybrid",
            }
        else:
            return {
                "recommendation": "unknown",
                "reason": "Database not found in configuration",
                "category": "uncategorized",
            }

    def _get_cloud_category(self, db_name: str) -> str:
        """Get the cloud storage category for a database"""
        for category, dbs in self.config["cloud_databases"].items():
            if isinstance(dbs, list) and db_name in dbs:
                return category
        return "unknown"

    def generate_migration_plan(self) -> Dict[str, Any]:
        """Generate a comprehensive migration plan"""
        plan = {
            "local_count": len(self.config["local_databases"]["performance_critical"]),
            "cloud_count": sum(
                len(dbs)
                for dbs in self.config["cloud_databases"].values()
                if isinstance(dbs, list)
            ),
            "evaluation_count": len(
                self.config["hybrid_databases"]["evaluate_case_by_case"]
            ),
            "migration_strategy": {
                "phase_1": "Keep performance-critical databases local",
                "phase_2": "Migrate analytics and business databases to cloud",
                "phase_3": "Evaluate hybrid databases based on usage patterns",
            },
            "estimated_storage_savings": "~80% reduction in local storage requirements",
        }
        return plan


class TaskCompletionDatabase:
    def __init__(self, db_path: str = "task_completion.db"):
        self.db_path = db_path
        self.conn: Optional[sqlite3.Connection] = None
        self.storage_manager = DatabaseStorageManager()
        self.initialize_database()

    def initialize_database(self):
        """Initialize the database with the schema"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row

            # Read and execute the schema
            schema_path = "task_completion_database.sql"
            if os.path.exists(schema_path):
                with open(schema_path, "r") as f:
                    schema = f.read()
                self.conn.executescript(schema)
                logger.info("Database schema initialized successfully")
            else:
                logger.error(f"Schema file {schema_path} not found")

        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            raise

    def add_task(
        self,
        task_name: str,
        description: str = None,
        category: str = "general",
        priority: str = "medium",
        parent_task_id: int = None,
        estimated_hours: float = None,
    ) -> int:
        """Add a new task to the database"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                INSERT INTO tasks (task_name, description, category, priority, parent_task_id, estimated_hours)
                VALUES (?, ?, ?, ?, ?, ?)
            """,
                (
                    task_name,
                    description,
                    category,
                    priority,
                    parent_task_id,
                    estimated_hours,
                ),
            )

            task_id = cursor.lastrowid
            self.conn.commit()
            logger.info(f"Added task: {task_name} (ID: {task_id})")
            return task_id

        except Exception as e:
            logger.error(f"Failed to add task {task_name}: {e}")
            self.conn.rollback()
            raise

    def update_task_status(
        self,
        task_id: int,
        status: str,
        completion_percentage: int = None,
        notes: str = None,
    ):
        """Update task status and completion percentage"""
        try:
            cursor = self.conn.cursor()

            update_fields = ["status = ?"]
            params = [status]

            if completion_percentage is not None:
                update_fields.append("completion_percentage = ?")
                params.append(completion_percentage)

            if notes:
                update_fields.append("notes = ?")
                params.append(notes)

            params.append(task_id)

            cursor.execute(
                f"""
                UPDATE tasks SET {', '.join(update_fields)}
                WHERE id = ?
            """,
                params,
            )

            self.conn.commit()
            logger.info(f"Updated task {task_id} status to {status}")

        except Exception as e:
            logger.error(f"Failed to update task {task_id}: {e}")
            self.conn.rollback()
            raise

    def add_file_issue(
        self,
        file_path: str,
        issue_type: str,
        issue_description: str,
        severity: str = "medium",
        forbidden_words: List[str] = None,
        line_numbers: List[int] = None,
    ):
        """Add a file with issues to track"""
        try:
            cursor = self.conn.cursor()

            forbidden_words_json = (
                json.dumps(forbidden_words) if forbidden_words else None
            )
            line_numbers_json = json.dumps(line_numbers) if line_numbers else None

            cursor.execute(
                """
                INSERT OR REPLACE INTO files_with_issues 
                (file_path, file_type, issue_type, issue_description, severity, 
                 forbidden_words, line_numbers)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    file_path,
                    self._get_file_type(file_path),
                    issue_type,
                    issue_description,
                    severity,
                    forbidden_words_json,
                    line_numbers_json,
                ),
            )

            self.conn.commit()
            logger.info(f"Added file issue: {file_path}")

        except Exception as e:
            logger.error(f"Failed to add file issue for {file_path}: {e}")
            self.conn.rollback()
            raise

    def add_project_component(
        self,
        component_name: str,
        component_type: str,
        file_path: str = None,
        description: str = None,
        dependencies: List[str] = None,
    ):
        """Add a project component to track"""
        try:
            cursor = self.conn.cursor()

            dependencies_json = json.dumps(dependencies) if dependencies else None

            cursor.execute(
                """
                INSERT INTO project_components 
                (component_name, component_type, file_path, description, dependencies)
                VALUES (?, ?, ?, ?, ?)
            """,
                (
                    component_name,
                    component_type,
                    file_path,
                    description,
                    dependencies_json,
                ),
            )

            component_id = cursor.lastrowid
            self.conn.commit()
            logger.info(f"Added component: {component_name} (ID: {component_id})")
            return component_id

        except Exception as e:
            logger.error(f"Failed to add component {component_name}: {e}")
            self.conn.rollback()
            raise

    def add_issue(
        self,
        issue_title: str,
        issue_description: str,
        issue_type: str,
        severity: str = "medium",
        component_id: int = None,
        file_path: str = None,
    ):
        """Add an issue to track"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                INSERT INTO issues 
                (issue_title, issue_description, issue_type, severity, component_id, file_path)
                VALUES (?, ?, ?, ?, ?, ?)
            """,
                (
                    issue_title,
                    issue_description,
                    issue_type,
                    severity,
                    component_id,
                    file_path,
                ),
            )

            issue_id = cursor.lastrowid
            self.conn.commit()
            logger.info(f"Added issue: {issue_title} (ID: {issue_id})")
            return issue_id

        except Exception as e:
            logger.error(f"Failed to add issue {issue_title}: {e}")
            self.conn.rollback()
            raise

    def parse_paste_content(self, paste_content_path: str):
        """Parse the paste_content.txt file and populate the database"""
        try:
            with open(paste_content_path, "r", encoding="utf-8") as f:
                content = f.read()

            logger.info("Parsing paste content...")

            # Extract files with forbidden vocabulary
            forbidden_files = self._extract_forbidden_files(content)
            for file_info in forbidden_files:
                self.add_file_issue(
                    file_path=file_info["path"],
                    issue_type="forbidden_vocabulary",
                    issue_description="Contains forbidden vocabulary that needs to be cleaned",
                    severity="high",
                    forbidden_words=file_info.get("words", []),
                )

            # Extract tasks and issues from conversations
            tasks = self._extract_tasks_from_content(content)
            for task in tasks:
                task_id = self.add_task(
                    task_name=task["name"],
                    description=task["description"],
                    category=task["category"],
                    priority=task["priority"],
                )

                # Add any related issues
                for issue in task.get("issues", []):
                    self.add_issue(
                        issue_title=issue["title"],
                        issue_description=issue["description"],
                        issue_type=issue["type"],
                        severity=issue["severity"],
                    )

            # Extract project components
            components = self._extract_components_from_content(content)
            for component in components:
                self.add_project_component(
                    component_name=component["name"],
                    component_type=component["type"],
                    file_path=component.get("file_path"),
                    description=component.get("description"),
                    dependencies=component.get("dependencies"),
                )

            logger.info("Paste content parsing completed")

        except Exception as e:
            logger.error(f"Failed to parse paste content: {e}")
            raise

    def _extract_forbidden_files(self, content: str) -> List[Dict[str, Any]]:
        """Extract files with forbidden vocabulary from content"""
        files = []

        # Look for file paths in the content
        file_patterns = [
            r"([^\s]+\.(py|js|html|css|md|json|yaml|yml|sql|sh|txt))",
            r"backup_[^/]+/([^\s]+)",
            r"([^\s]*templates[^\s]*)",
            r"([^\s]*monitoring[^\s]*)",
        ]

        for pattern in file_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                file_path = match if isinstance(match, str) else match[0]
                if file_path and len(file_path) > 3:  # Filter out very short matches
                    files.append(
                        {
                            "path": file_path,
                            "words": [
                                "profanity",
                                "inappropriate_language",
                            ],  # Generic placeholder
                        }
                    )

        return files

    def _extract_tasks_from_content(self, content: str) -> List[Dict[str, Any]]:
        """Extract tasks and issues from the content"""
        tasks = []

        # Common task indicators
        task_patterns = [
            r"(?i)(fix|resolve|implement|create|build|deploy|test|update|configure)",
            r"(?i)(todo|task|issue|problem|error|bug)",
            r"(?i)(needs? to|should|must|require[ds]?)",
        ]

        lines = content.split("\n")
        for i, line in enumerate(lines):
            line = line.strip()
            if len(line) < 10:  # Skip very short lines
                continue

            for pattern in task_patterns:
                if re.search(pattern, line):
                    # Extract context around the line
                    context_start = max(0, i - 2)
                    context_end = min(len(lines), i + 3)
                    context = " ".join(lines[context_start:context_end])

                    task = {
                        "name": line[:100],  # Truncate long names
                        "description": context[:500],  # Truncate long descriptions
                        "category": self._categorize_task(line),
                        "priority": self._prioritize_task(line),
                        "issues": [],
                    }

                    # Look for related issues
                    if any(
                        word in line.lower()
                        for word in ["error", "bug", "fail", "broken"]
                    ):
                        task["issues"].append(
                            {
                                "title": f"Issue in: {line[:50]}",
                                "description": context[:300],
                                "type": "bug",
                                "severity": "medium",
                            }
                        )

                    tasks.append(task)
                    break

        return tasks[:50]  # Limit to first 50 tasks to avoid overwhelming

    def _extract_components_from_content(self, content: str) -> List[Dict[str, Any]]:
        """Extract project components from content"""
        components = []

        # Look for common component types
        component_patterns = {
            "service": r"(?i)(service|server|api|endpoint)",
            "database": r"(?i)(database|db|sql|sqlite|postgres|mysql)",
            "frontend": r"(?i)(frontend|ui|interface|web|html|css|js)",
            "backend": r"(?i)(backend|server|api|service)",
            "deployment": r"(?i)(deploy|docker|container|k8s|kubernetes)",
            "monitoring": r"(?i)(monitor|log|metric|health|status)",
            "security": r"(?i)(security|auth|permission|access|token)",
            "configuration": r"(?i)(config|setting|environment|env)",
        }

        lines = content.split("\n")
        for line in lines:
            line = line.strip()
            if len(line) < 5:
                continue

            for comp_type, pattern in component_patterns.items():
                if re.search(pattern, line):
                    # Extract potential file path
                    file_match = re.search(
                        r"([^\s]+\.(py|js|html|css|json|yaml|yml|sql|sh))", line
                    )
                    file_path = file_match.group(1) if file_match else None

                    component = {
                        "name": line[:100],
                        "type": comp_type,
                        "file_path": file_path,
                        "description": line[:200],
                        "dependencies": [],
                    }
                    components.append(component)
                    break

        return components[:30]  # Limit to avoid overwhelming

    def _categorize_task(self, task_text: str) -> str:
        """Categorize a task based on its content"""
        task_lower = task_text.lower()

        if any(word in task_lower for word in ["deploy", "production", "release"]):
            return "deployment"
        elif any(word in task_lower for word in ["test", "verify", "validate"]):
            return "testing"
        elif any(word in task_lower for word in ["fix", "bug", "error", "issue"]):
            return "bugfix"
        elif any(word in task_lower for word in ["security", "auth", "permission"]):
            return "security"
        elif any(word in task_lower for word in ["config", "setting", "environment"]):
            return "configuration"
        elif any(word in task_lower for word in ["ui", "frontend", "interface"]):
            return "frontend"
        elif any(word in task_lower for word in ["api", "backend", "server"]):
            return "backend"
        else:
            return "general"

    def _prioritize_task(self, task_text: str) -> str:
        """Determine task priority based on content"""
        task_lower = task_text.lower()

        if any(
            word in task_lower
            for word in ["critical", "urgent", "emergency", "broken", "down"]
        ):
            return "high"
        elif any(
            word in task_lower for word in ["important", "security", "production"]
        ):
            return "high"
        elif any(word in task_lower for word in ["should", "improve", "optimize"]):
            return "medium"
        else:
            return "medium"

    def _get_file_type(self, file_path: str) -> str:
        """Get file type from file path"""
        if "." not in file_path:
            return "unknown"

        extension = file_path.split(".")[-1].lower()

        type_mapping = {
            "py": "python",
            "js": "javascript",
            "html": "html",
            "css": "css",
            "json": "json",
            "yaml": "yaml",
            "yml": "yaml",
            "sql": "sql",
            "md": "markdown",
            "txt": "text",
            "sh": "shell",
            "dockerfile": "docker",
        }

        return type_mapping.get(extension, extension)

    def get_incomplete_tasks(self) -> List[Dict[str, Any]]:
        """Get all incomplete tasks"""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT * FROM incomplete_tasks ORDER BY priority DESC, created_at ASC"
        )
        return [dict(row) for row in cursor.fetchall()]

    def get_critical_issues(self) -> List[Dict[str, Any]]:
        """Get all critical issues"""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT * FROM critical_issues ORDER BY severity DESC, created_at ASC"
        )
        return [dict(row) for row in cursor.fetchall()]

    def get_files_needing_fixes(self) -> List[Dict[str, Any]]:
        """Get all files that need fixes"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM files_needing_fixes ORDER BY severity DESC")
        return [dict(row) for row in cursor.fetchall()]

    def get_completion_summary(self) -> Dict[str, Any]:
        """Get overall completion summary"""
        cursor = self.conn.cursor()

        # Task summary
        cursor.execute(
            """
            SELECT 
                status,
                COUNT(*) as count,
                AVG(completion_percentage) as avg_completion
            FROM tasks 
            GROUP BY status
        """
        )
        task_summary = {
            row["status"]: {
                "count": row["count"],
                "avg_completion": row["avg_completion"],
            }
            for row in cursor.fetchall()
        }

        # Issue summary
        cursor.execute(
            """
            SELECT 
                status,
                severity,
                COUNT(*) as count
            FROM issues 
            GROUP BY status, severity
        """
        )
        issue_summary = {}
        for row in cursor.fetchall():
            if row["status"] not in issue_summary:
                issue_summary[row["status"]] = {}
            issue_summary[row["status"]][row["severity"]] = row["count"]

        # File issues summary
        cursor.execute(
            """
            SELECT 
                status,
                COUNT(*) as count
            FROM files_with_issues 
            GROUP BY status
        """
        )
        file_summary = {row["status"]: row["count"] for row in cursor.fetchall()}

        return {
            "tasks": task_summary,
            "issues": issue_summary,
            "files": file_summary,
            "generated_at": datetime.now().isoformat(),
        }

    def force_complete_task(
        self, task_id: int, completion_notes: str = "Forced completion"
    ):
        """Force complete a task with validation"""
        try:
            # Add validation record
            cursor = self.conn.cursor()
            cursor.execute(
                """
                INSERT INTO completion_validations 
                (task_id, validation_type, validation_criteria, validation_result, 
                 validated_by, validated_at, validation_notes)
                VALUES (?, 'manual', 'Forced completion by system', 'pass', 'system', ?, ?)
            """,
                (task_id, datetime.now(), completion_notes),
            )

            # Update task to completed
            self.update_task_status(task_id, "completed", 100, completion_notes)

            logger.info(f"Force completed task {task_id}")

        except Exception as e:
            logger.error(f"Failed to force complete task {task_id}: {e}")
            raise

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed")


def main():
    """Main function to initialize and populate the database"""
    try:
        # Initialize database
        db = TaskCompletionDatabase()

        # Parse paste content if it exists
        paste_content_path = "paste_content.txt"
        if os.path.exists(paste_content_path):
            logger.info("Found paste_content.txt, parsing...")
            db.parse_paste_content(paste_content_path)
        else:
            logger.warning("paste_content.txt not found, creating sample data...")

            # Create some sample tasks to demonstrate the system
            sample_tasks = [
                {
                    "name": "Fix all forbidden vocabulary in files",
                    "description": "Clean up all files containing inappropriate language",
                    "category": "cleanup",
                    "priority": "high",
                },
                {
                    "name": "Complete deployment setup",
                    "description": "Ensure all deployment configurations are complete",
                    "category": "deployment",
                    "priority": "high",
                },
                {
                    "name": "Validate all project components",
                    "description": "Test and validate all project components are working",
                    "category": "testing",
                    "priority": "medium",
                },
            ]

            for task in sample_tasks:
                db.add_task(**task)

        # Generate completion summary
        summary = db.get_completion_summary()
        logger.info("=== COMPLETION SUMMARY ===")
        logger.info(json.dumps(summary, indent=2))

        # Show incomplete tasks
        incomplete = db.get_incomplete_tasks()
        logger.info(f"\n=== INCOMPLETE TASKS ({len(incomplete)}) ===")
        for task in incomplete[:10]:  # Show first 10
            logger.info(
                f"- {task['task_name']} ({task['status']}, {task['completion_percentage']}%)"
            )

        # Show critical issues
        critical = db.get_critical_issues()
        logger.info(f"\n=== CRITICAL ISSUES ({len(critical)}) ===")
        for issue in critical[:10]:  # Show first 10
            logger.info(f"- {issue['issue_title']} ({issue['severity']})")

        # Show files needing fixes
        files = db.get_files_needing_fixes()
        logger.info(f"\n=== FILES NEEDING FIXES ({len(files)}) ===")
        for file_info in files[:10]:  # Show first 10
            logger.info(f"- {file_info['file_path']} ({file_info['issue_type']})")

        logger.info("\n=== DATABASE READY ===")
        logger.info("The task completion database is now ready to track EVERY task")
        logger.info("and ensure NOTHING is left incomplete!")

        db.close()

    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise


if __name__ == "__main__":
    main()
