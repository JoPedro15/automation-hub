# 🛠️ Core Library (core-lib)

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/release/python-3120/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

The shared foundation of the **Automation Hub**. This library provides fundamental cross-domain utilities that ensure
consistency across all automation clients and AI research labs.

## ⚙️ Features

- **Standardized Logging**: Unified ANSI-colored output with precise timestamps.
- **No-Print Policy**: Enforces the removal of raw `print` statements via the `Logger` service.
- **Clean Terminal UI**: Professional headers and section markers for pipeline orchestration.
- **Production-Ready**: Thread-safe terminal output using `sys.stderr` for errors.

## 🏗 Key Components

### 📝 Logger Client

The `Logger` provides a clean, emoji-free interface for terminal communication. It automatically includes
timestamps and color-coded status levels.

```python
from clients.core_lib.core_lib_client.logger_client import logger

# Section headers for pipeline stages
logger.section("Data Ingestion Stage")  #

# Standard logging levels
logger.info("Initializing connection to GDrive...")  #
logger.success("File downloaded successfully.")  #
logger.warning("Optional dependency 'X' missing. Using default settings.")  #
logger.error("Authentication failed: invalid token.")  #
```

## 📋 API ReferenceMethodDescriptionOutput

| Method           | Description                         | Output Format                                 |
| :--------------- | :---------------------------------- | :-------------------------------------------- |
| `info(msg)`      | Standard information log.           | `[YYYY-MM-DD HH:MM:SS] INFO: msg`             |
| `success(msg)`   | Positive outcome notification.      | `[YYYY-MM-DD HH:MM:SS] SUCCESS: msg (Green)`  |
| `warning(msg)`   | Alerts for potential issues.        | `[YYYY-MM-DD HH:MM:SS] WARNING: msg (Yellow)` |
| `error(msg)`     | Critical failures (sent to stderr). | `[YYYY-MM-DD HH:MM:SS] ERROR: msg (Red)`      |
| `section(title)` | Major pipeline milestone markers.   | `Uppercase bold header with line break`       |

## 🧪 Quality & Standards

This library defines the standards for the entire ecosystem. It is strictly monitored by our global quality gate:

Linter (Ruff): All print statements in this client are explicitly tagged with # noqa: T201 as they
are part of the core logging engine.

Security (Bandit): Scanned for secure handling of output streams.

Pre-commit Hooks: Enforces trailing whitespace removal, end-of-file fixers, and YAML validation for config files.

## 🛠 Setup

Managed as an editable package within the automation-hub:

```Bash
# Core installation used by all other clients
cd clients/core_lib
pip install -e .
```

______________________________________________________________________

**João Pedro** | Automation Engineer
<br />
[GitHub](https://github.com/JoPedro15) • [Automation Hub](https://github.com/JoPedro15/automation-hub) • [AI Lab](https://github.com/JoPedro15/ai-lab)
<br />
