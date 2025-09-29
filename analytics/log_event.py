#!/usr/bin/env python3
"""
Analytics Event Logger
SQLite-based analytics system for tracking application metrics
"""

import json
import os
import sqlite3
import sys
from datetime import datetime
from pathlib import Path


class AnalyticsLogger:
    def __init__(self, db_path='analytics/telemetry.sqlite'):
        """Initialize analytics logger with SQLite database"""
        
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.init_database()
    
    def init_database(self):
        """Initialize SQLite database with required tables"""
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Events table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    event_type TEXT NOT NULL,
                    event_data TEXT,
                    source TEXT,
                    session_id TEXT,
                    user_id TEXT,
                    metadata TEXT
                )
            ''')
            
            # Metrics table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    metric_name TEXT NOT NULL,
                    metric_value REAL NOT NULL,
                    metric_unit TEXT,
                    source TEXT,
                    tags TEXT
                )
            ''')
            
            # Sessions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sessions (
                    id TEXT PRIMARY KEY,
                    start_time TEXT NOT NULL,
                    end_time TEXT,
                    duration_seconds INTEGER,
                    event_count INTEGER DEFAULT 0,
                    source TEXT,
                    metadata TEXT
                )
            ''')
            
            # Performance table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS performance (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    operation TEXT NOT NULL,
                    duration_ms REAL NOT NULL,
                    success BOOLEAN NOT NULL,
                    error_message TEXT,
                    source TEXT,
                    metadata TEXT
                )
            ''')
            
            # Create indexes for better performance
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_events_timestamp ON events(timestamp)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_events_type ON events(event_type)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_metrics_timestamp ON metrics(timestamp)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_metrics_name ON metrics(metric_name)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_performance_timestamp ON performance(timestamp)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_performance_operation ON performance(operation)')
            
            conn.commit()
    
    def log_event(self, event_type, event_data=None, source=None, session_id=None, user_id=None, metadata=None):
        """Log an event to the analytics database"""
        
        timestamp = datetime.now().isoformat()
        
        # Convert data to JSON string if it's a dict/list
        if isinstance(event_data, (dict, list)):
            event_data = json.dumps(event_data)
        
        if isinstance(metadata, (dict, list)):
            metadata = json.dumps(metadata)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO events (timestamp, event_type, event_data, source, session_id, user_id, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (timestamp, event_type, event_data, source, session_id, user_id, metadata))
            conn.commit()
        
        print(f"📊 Logged event: {event_type}")
    
    def log_metric(self, metric_name, metric_value, metric_unit=None, source=None, tags=None):
        """Log a metric to the analytics database"""
        
        timestamp = datetime.now().isoformat()
        
        if isinstance(tags, (dict, list)):
            tags = json.dumps(tags)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO metrics (timestamp, metric_name, metric_value, metric_unit, source, tags)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (timestamp, metric_name, metric_value, metric_unit, source, tags))
            conn.commit()
        
        print(f"📈 Logged metric: {metric_name} = {metric_value} {metric_unit or ''}")
    
    def log_performance(self, operation, duration_ms, success=True, error_message=None, source=None, metadata=None):
        """Log performance metrics"""
        
        timestamp = datetime.now().isoformat()
        
        if isinstance(metadata, (dict, list)):
            metadata = json.dumps(metadata)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO performance (timestamp, operation, duration_ms, success, error_message, source, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (timestamp, operation, duration_ms, success, error_message, source, metadata))
            conn.commit()
        
        status = "✅" if success else "❌"
        print(f"⚡ {status} Performance: {operation} = {duration_ms:.2f}ms")
    
    def get_metrics_summary(self, hours=24):
        """Get metrics summary for the last N hours"""
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Get event counts by type
            cursor.execute('''
                SELECT event_type, COUNT(*) as count
                FROM events
                WHERE timestamp >= datetime('now', '-{} hours')
                GROUP BY event_type
                ORDER BY count DESC
            '''.format(hours))
            
            events = cursor.fetchall()
            
            # Get metric averages
            cursor.execute('''
                SELECT metric_name, AVG(metric_value) as avg_value, COUNT(*) as count
                FROM metrics
                WHERE timestamp >= datetime('now', '-{} hours')
                GROUP BY metric_name
                ORDER BY count DESC
            '''.format(hours))
            
            metrics = cursor.fetchall()
            
            # Get performance summary
            cursor.execute('''
                SELECT operation, AVG(duration_ms) as avg_duration, COUNT(*) as count,
                       SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as success_count
                FROM performance
                WHERE timestamp >= datetime('now', '-{} hours')
                GROUP BY operation
                ORDER BY avg_duration DESC
            '''.format(hours))
            
            performance = cursor.fetchall()
            
            return {
                'events': events,
                'metrics': metrics,
                'performance': performance
            }
    
    def export_data(self, output_file, format='json'):
        """Export analytics data to file"""
        
        summary = self.get_metrics_summary()
        
        if format == 'json':
            with open(output_file, 'w') as f:
                json.dump(summary, f, indent=2)
        elif format == 'csv':
            # TODO: Implement CSV export
            pass
        
        print(f"📤 Exported analytics data to {output_file}")

def main():
    """Command line interface for analytics logging"""
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 log_event.py event <type> [data] [source]")
        print("  python3 log_event.py metric <name> <value> [unit] [source]")
        print("  python3 log_event.py performance <operation> <duration_ms> [success] [source]")
        print("  python3 log_event.py summary [hours]")
        print("  python3 log_event.py export <output_file> [format]")
        print("")
        print("Examples:")
        print("  python3 log_event.py event 'user_login' '{\"user_id\": \"123\"}' 'web'")
        print("  python3 log_event.py metric 'revenue' 1250.50 'USD' 'business'")
        print("  python3 log_event.py performance 'video_render' 1500.25 true 'pipeline'")
        print("  python3 log_event.py summary 24")
        print("  python3 log_event.py export analytics.json")
        sys.exit(1)
    
    logger = AnalyticsLogger()
    command = sys.argv[1]
    
    if command == 'event':
        if len(sys.argv) < 3:
            print("❌ Event command requires event type")
            sys.exit(1)
        
        event_type = sys.argv[2]
        event_data = sys.argv[3] if len(sys.argv) > 3 else None
        source = sys.argv[4] if len(sys.argv) > 4 else None
        
        # Try to parse JSON data
        if event_data:
            try:
                event_data = json.loads(event_data)
            except json.JSONDecodeError:
                pass  # Keep as string
        
        logger.log_event(event_type, event_data, source)
    
    elif command == 'metric':
        if len(sys.argv) < 4:
            print("❌ Metric command requires name and value")
            sys.exit(1)
        
        metric_name = sys.argv[2]
        metric_value = float(sys.argv[3])
        metric_unit = sys.argv[4] if len(sys.argv) > 4 else None
        source = sys.argv[5] if len(sys.argv) > 5 else None
        
        logger.log_metric(metric_name, metric_value, metric_unit, source)
    
    elif command == 'performance':
        if len(sys.argv) < 4:
            print("❌ Performance command requires operation and duration")
            sys.exit(1)
        
        operation = sys.argv[2]
        duration_ms = float(sys.argv[3])
        success = sys.argv[4].lower() == 'true' if len(sys.argv) > 4 else True
        source = sys.argv[5] if len(sys.argv) > 5 else None
        
        logger.log_performance(operation, duration_ms, success, source=source)
    
    elif command == 'summary':
        hours = int(sys.argv[2]) if len(sys.argv) > 2 else 24
        summary = logger.get_metrics_summary(hours)
        
        print(f"\n📊 Analytics Summary (Last {hours} hours)")
        print("=" * 50)
        
        print("\n📈 Events:")
        for event_type, count in summary['events']:
            print(f"  {event_type}: {count}")
        
        print("\n📊 Metrics:")
        for metric_name, avg_value, count in summary['metrics']:
            print(f"  {metric_name}: {avg_value:.2f} (avg, {count} samples)")
        
        print("\n⚡ Performance:")
        for operation, avg_duration, count, success_count in summary['performance']:
            success_rate = (success_count / count * 100) if count > 0 else 0
            print(f"  {operation}: {avg_duration:.2f}ms avg ({success_rate:.1f}% success)")
    
    elif command == 'export':
        if len(sys.argv) < 3:
            print("❌ Export command requires output file")
            sys.exit(1)
        
        output_file = sys.argv[2]
        format = sys.argv[3] if len(sys.argv) > 3 else 'json'
        
        logger.export_data(output_file, format)
    
    else:
        print(f"❌ Unknown command: {command}")
        sys.exit(1)

if __name__ == '__main__':
    main()
