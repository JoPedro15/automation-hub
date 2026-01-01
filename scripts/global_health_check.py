import sys
from typing import Callable, List, Tuple

from clients.core_lib.core_lib_client.logger_client import logger
from clients.gdrive.scripts.gdrive_health_check import run_gdrive_check

# ANSI Color codes for terminal feedback
GREEN: str = "\033[92m"
RED: str = "\033[91m"
RESET: str = "\033[0m"
BOLD: str = "\033[1m"


def run_all_health_checks() -> None:
    """
    Orchestrates all health checks and enforces exit codes based on results.
    """
    logger.section(">>> Orchestrating Global Health Checks...")

    checks: List[Tuple[str, Callable[[], Tuple[bool, str]]]] = [
        ("Google Drive Unit", run_gdrive_check),
    ]

    failed: bool = False

    for name, func in checks:
        success, message = func()
        status_color: str = GREEN if success else RED
        status_text: str = "OK" if success else "FAIL"

        logger.info(f"[{status_color}{status_text}{RESET}] {name}: {message}")

        if not success:
            failed = True

    if failed:
        error_msg: str = (
            f"\n{RED}{BOLD}>>> ❌ Health Check Failed: "
            f"One or more integrations are unreachable.{RESET}"
        )
        print(error_msg)
        sys.exit(1)
    else:
        logger.success(f">>> ✅ All systems functional.{RESET}")
        sys.exit(0)


if __name__ == "__main__":
    run_all_health_checks()
