#!/usr/bin/env python3
"""
Base44 Auto-Sync Daemon
Runs Base44 synchronization automatically at regular intervals
"""

import time
import signal
import sys
import os
import logging
from pathlib import Path

sys.path.append(str(Path(__file__).parent))
from base44_sync import Base44Sync

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("auto_sync_daemon.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


class AutoSyncDaemon:
    def __init__(self, sync_interval: int = 300):
        self.sync_interval = sync_interval
        self.running = True
        self.sync = Base44Sync()

        # Set up signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

    def signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        logger.info(f"Received signal {signum}, shutting down gracefully...")
        self.running = False

    def run(self):
        """Main daemon loop"""
        logger.info(
            f"Starting Base44 Auto-Sync Daemon (interval: {self.sync_interval}s)"
        )

        while self.running:
            try:
                logger.info("Checking for Base44 updates...")

                if self.sync.check_base44_updates():
                    logger.info("Updates detected, starting synchronization...")
                    success = self.sync.run_sync()

                    if success:
                        logger.info("Synchronization completed successfully")
                    else:
                        logger.error("Synchronization failed")
                else:
                    logger.info("No updates found")

                # Wait for next check
                for _ in range(self.sync_interval):
                    if not self.running:
                        break
                    time.sleep(1)

            except Exception as e:
                logger.error(f"Error in daemon loop: {e}")
                time.sleep(60)  # Wait a minute before retrying

        logger.info("Auto-Sync Daemon stopped")


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="Base44 Auto-Sync Daemon")
    parser.add_argument(
        "--interval",
        type=int,
        default=300,
        help="Sync check interval in seconds (default: 300)",
    )
    parser.add_argument(
        "--daemon", action="store_true", help="Run as daemon (detach from terminal)"
    )

    args = parser.parse_args()

    if args.daemon:
        # Simple daemonization (for production, consider using proper daemon libraries)
        try:
            pid = os.fork()
            if pid > 0:
                # Parent process exits
                sys.exit(0)
        except OSError as e:
            logger.error(f"Fork failed: {e}")
            sys.exit(1)

        # Detach from controlling terminal
        os.setsid()

        # Second fork to prevent zombie processes
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError as e:
            logger.error(f"Second fork failed: {e}")
            sys.exit(1)

    daemon = AutoSyncDaemon(sync_interval=args.interval)
    daemon.run()


if __name__ == "__main__":
    main()
