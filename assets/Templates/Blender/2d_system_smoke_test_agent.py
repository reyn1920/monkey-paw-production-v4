"""
System Smoke Test Agent

This module provides automated system health monitoring and smoke testing capabilities
for the TRAE.AI dashboard system.
"""

import asyncio
import logging
import time
from datetime import datetime, timezone
from dataclasses import dataclass
from enum import Enum
import aiohttp
import psutil
import sqlite3

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AgentStatus(Enum):
    """Agent status enumeration"""

    IDLE = "idle"
    RUNNING = "running"
    PAUSED = "paused"
    ERROR = "error"
    STOPPED = "stopped"


class TestResult(Enum):
    """Test result enumeration"""

    PASS = "pass"
    FAIL = "fail"
    WARNING = "warning"
    SKIP = "skip"


@dataclass
class SmokeTestResult:
    """Smoke test result data structure"""

    test_name: str
    status: TestResult
    message: str
    duration: float
    timestamp: datetime
    details: Optional[dict[str, Any]] = None


@dataclass
class SystemMetrics:
    """System metrics data structure"""

    cpu_usage: float
    memory_usage: float
    disk_usage: float
    network_status: bool
    database_status: bool
    timestamp: datetime


class SystemSmokeTestAgent:
    """
    System Smoke Test Agent for monitoring system health and running automated tests
    """

    def __init__(self, config: Optional[dict[str, Any]] = None):
        self.config = config or {}
        self.status = AgentStatus.IDLE
        self.test_results: list[SmokeTestResult] = []
        self.last_run: Optional[datetime] = None
        self.running = False

    async def start(self):
        """Start the smoke test agent"""
        logger.info("Starting System Smoke Test Agent")
        self.status = AgentStatus.RUNNING
        self.running = True

        # Run initial smoke tests
        await self.run_smoke_tests()

    async def stop(self):
        """Stop the smoke test agent"""
        logger.info("Stopping System Smoke Test Agent")
        self.running = False
        self.status = AgentStatus.STOPPED

    async def pause(self):
        """Pause the smoke test agent"""
        logger.info("Pausing System Smoke Test Agent")
        self.status = AgentStatus.PAUSED

    async def resume(self):
        """Resume the smoke test agent"""
        logger.info("Resuming System Smoke Test Agent")
        self.status = AgentStatus.RUNNING

    async def run_smoke_tests(self) -> list[SmokeTestResult]:
        """Run all smoke tests"""
        if self.status != AgentStatus.RUNNING:
            return self.test_results

        logger.info("Running smoke tests")
        self.test_results.clear()

        # Run individual tests
        tests = [
            self._test_system_resources,
            self._test_database_connectivity,
            self._test_network_connectivity,
            self._test_file_system,
            self._test_application_endpoints,
        ]

        for test in tests:
            try:
                result = await test()
                self.test_results.append(result)
            except Exception as e:
                logger.error(f"Error running test {test.__name__}: {e}")
                self.test_results.append(
                    SmokeTestResult(
                        test_name=test.__name__,
                        status=TestResult.FAIL,
                        message=f"Test failed with exception: {str(e)}",
                        duration=0.0,
                        timestamp=datetime.now(timezone.utc),
                    )
                )

        self.last_run = datetime.now(timezone.utc)
        return self.test_results

    async def _test_system_resources(self) -> SmokeTestResult:
        """Test system resource usage"""
        start_time = time.time()

        try:
            cpu_usage = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage("/")

            # Check thresholds
            warnings = []
            if cpu_usage > 80:
                warnings.append(f"High CPU usage: {cpu_usage}%")
            if memory.percent > 85:
                warnings.append(f"High memory usage: {memory.percent}%")
            if disk.percent > 90:
                warnings.append(f"High disk usage: {disk.percent}%")

            status = TestResult.WARNING if warnings else TestResult.PASS
            message = (
                "; ".join(warnings)
                if warnings
                else "System resources within normal limits"
            )

            return SmokeTestResult(
                test_name="system_resources",
                status=status,
                message=message,
                duration=time.time() - start_time,
                timestamp=datetime.now(timezone.utc),
                details={
                    "cpu_usage": cpu_usage,
                    "memory_usage": memory.percent,
                    "disk_usage": disk.percent,
                },
            )

        except Exception as e:
            return SmokeTestResult(
                test_name="system_resources",
                status=TestResult.FAIL,
                message=f"Failed to check system resources: {str(e)}",
                duration=time.time() - start_time,
                timestamp=datetime.now(timezone.utc),
            )

    async def _test_database_connectivity(self) -> SmokeTestResult:
        """Test database connectivity"""
        start_time = time.time()

        try:
            # Test SQLite database connection
            db_path = self.config.get("database_path", "dashboard.db")
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            conn.close()

            if result and result[0] == 1:
                return SmokeTestResult(
                    test_name="database_connectivity",
                    status=TestResult.PASS,
                    message="Database connection successful",
                    duration=time.time() - start_time,
                    timestamp=datetime.now(timezone.utc),
                )
            else:
                return SmokeTestResult(
                    test_name="database_connectivity",
                    status=TestResult.FAIL,
                    message="Database query returned unexpected result",
                    duration=time.time() - start_time,
                    timestamp=datetime.now(timezone.utc),
                )

        except Exception as e:
            return SmokeTestResult(
                test_name="database_connectivity",
                status=TestResult.FAIL,
                message=f"Database connection failed: {str(e)}",
                duration=time.time() - start_time,
                timestamp=datetime.now(timezone.utc),
            )

    async def _test_network_connectivity(self) -> SmokeTestResult:
        """Test network connectivity"""
        start_time = time.time()

        try:
            timeout = aiohttp.ClientTimeout(total=5)
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    "http://httpbin.org/status/200", timeout=timeout
                ) as response:
                    if response.status == 200:
                        return SmokeTestResult(
                            test_name="network_connectivity",
                            status=TestResult.PASS,
                            message="Network connectivity test passed",
                            duration=time.time() - start_time,
                            timestamp=datetime.now(timezone.utc),
                        )
                    else:
                        return SmokeTestResult(
                            test_name="network_connectivity",
                            status=TestResult.FAIL,
                            message=f"Network test returned status {
                                response.status}",
                            duration=time.time() - start_time,
                            timestamp=datetime.now(timezone.utc),
                        )

        except Exception as e:
            return SmokeTestResult(
                test_name="network_connectivity",
                status=TestResult.FAIL,
                message=f"Network connectivity test failed: {str(e)}",
                duration=time.time() - start_time,
                timestamp=datetime.now(timezone.utc),
            )

    async def _test_file_system(self) -> SmokeTestResult:
        """Test file system operations"""
        start_time = time.time()

        try:
            # Test write/read operations
            test_file = "/tmp/smoke_test_file.txt"
            test_content = "smoke test content"

            # Write test
            with open(test_file, "w") as f:
                f.write(test_content)

            # Read test
            with open(test_file) as f:
                content = f.read()

            # Cleanup
            import os

            os.remove(test_file)

            if content == test_content:
                return SmokeTestResult(
                    test_name="file_system",
                    status=TestResult.PASS,
                    message="File system operations successful",
                    duration=time.time() - start_time,
                    timestamp=datetime.now(timezone.utc),
                )
            else:
                return SmokeTestResult(
                    test_name="file_system",
                    status=TestResult.FAIL,
                    message="File system read/write test failed",
                    duration=time.time() - start_time,
                    timestamp=datetime.now(timezone.utc),
                )

        except Exception as e:
            return SmokeTestResult(
                test_name="file_system",
                status=TestResult.FAIL,
                message=f"File system test failed: {str(e)}",
                duration=time.time() - start_time,
                timestamp=datetime.now(timezone.utc),
            )

    async def _test_application_endpoints(self) -> SmokeTestResult:
        """Test application endpoints"""
        start_time = time.time()

        try:
            # Test local application endpoint
            timeout = aiohttp.ClientTimeout(total=5)
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    "http://localhost:8000", timeout=timeout
                ) as response:
                    if response.status == 200:
                        return SmokeTestResult(
                            test_name="application_endpoints",
                            status=TestResult.PASS,
                            message="Application endpoint test passed",
                            duration=time.time() - start_time,
                            timestamp=datetime.now(timezone.utc),
                        )
                    else:
                        return SmokeTestResult(
                            test_name="application_endpoints",
                            status=TestResult.WARNING,
                            message=f"Application endpoint returned status {
                                response.status}",
                            duration=time.time() - start_time,
                            timestamp=datetime.now(timezone.utc),
                        )

        except Exception as e:
            return SmokeTestResult(
                test_name="application_endpoints",
                status=TestResult.WARNING,
                message=f"Application endpoint test failed: {str(e)}",
                duration=time.time() - start_time,
                timestamp=datetime.now(timezone.utc),
            )

    def get_status(self) -> dict[str, Any]:
        """Get agent status"""
        return {
            "status": self.status.value,
            "last_run": self.last_run.isoformat() if self.last_run else None,
            "test_count": len(self.test_results),
            "passed_tests": len(
                [r for r in self.test_results if r.status == TestResult.PASS]
            ),
            "failed_tests": len(
                [r for r in self.test_results if r.status == TestResult.FAIL]
            ),
            "warning_tests": len(
                [r for r in self.test_results if r.status == TestResult.WARNING]
            ),
        }

    def get_test_results(self) -> list[dict[str, Any]]:
        """Get test results as dictionaries"""
        return [
            {
                "test_name": result.test_name,
                "status": result.status.value,
                "message": result.message,
                "duration": result.duration,
                "timestamp": result.timestamp.isoformat(),
                "details": result.details,
            }
            for result in self.test_results
        ]


# Global agent instance
smoke_test_agent = SystemSmokeTestAgent()


async def main():
    """Main function for testing"""
    agent = SystemSmokeTestAgent()
    await agent.start()
    results = await agent.run_smoke_tests()

    print("Smoke Test Results:")
    for result in results:
        print(f"  {result.test_name}: {result.status.value} - {result.message}")


if __name__ == "__main__":
    asyncio.run(main())
