#!/usr/bin/env python3
"""
Database migration script to add reports table
"""

import sqlite3
import os


def create_reports_table():
    """Create the reports table in the database"""
    db_path = os.path.join(os.path.dirname(__file__), "database.db")

    conn = None
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Create reports table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                report_type TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                data TEXT,
                file_path TEXT,
                generated_by TEXT
            )
        """
        )

        # Create index for faster queries
        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_reports_type
            ON reports(report_type)
        """
        )

        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_reports_status
            ON reports(status)
        """
        )

        conn.commit()
        print("Reports table created successfully")

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        if conn:
            conn.close()

    return True


if __name__ == "__main__":
    create_reports_table()
