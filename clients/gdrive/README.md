# 📂 Google Drive Client

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/release/python-3120/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Security: Bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)

A standalone infrastructure connector for Google Drive API, designed for the **Automation Hub** ecosystem.

It provides a standardized interface for file orchestration, abstracting the complexity of the Google Discovery API.

## ⚙️ Features

- **OAuth2 Flow**: Handled via `service_account` or `authorized_user` with automatic token refresh.
- **Promotion Pattern**: Clean imports via package root for high-level orchestration.
- **Type Safety**: Fully annotated methods for robust automation pipelines.
- **Resilient Operations**: Built-in retry logic and custom exception mapping for API 40x/50x errors.

## 📋 Prerequisites

Before initialization, ensure you have:

1. A **Google Cloud Project** with the Drive API enabled.
1. A `credentials.json` file placed in the `data/` directory.
1. Python 3.12+ installed.

## 🛠 Installation & Development

This client is managed by the root `automation-hub` orchestrator but can be developed independently:

```bash
# From the project root
make setup

# Or specifically for this client
cd clients/gdrive
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## 🏗 Usage

The Promotion Pattern
Leveraging the promotion pattern, you should import the client directly from the package root to
maintain clean orchestration layers:

```python
from clients.gdrive import GDriveClient

# Initialize with explicit credentials path
client: GDriveClient = GDriveClient(credentials_path="data/credentials.json")

# We use 'folder_id' as defined in the client's method signature
files: list[dict] = client.list_files(
    folder_id="1abc123_your_folder_id_here",
    limit=5
)
```

### Core API Reference

| Method          | Signature                           | Description                                        |
| :-------------- | :---------------------------------- | :------------------------------------------------- |
| `upload_file`   | `(src: str, folder_id: str) -> str` | Uploads local file and returns the GDrive File ID. |
| `download_file` | `(file_id: str, dest: str) -> None` | Downloads a remote file to a local destination.    |
| `list_files`    | `(query: str) -> list[dict]`        | Returns a list of file objects matching the query. |
| `delete_file`   | `(file_id: str) -> None`            | Moves a file to trash or deletes it permanently.   |

## 🧪 Testing

We use `pytest` with a heavy focus on mocking the `google-api-python-client` to ensure fast and reliable unit tests.

```Bash
# Run all GDrive tests
make test-all
```

## 🛡️ Security & Environment

Credential Isolation: All JSON secrets are strictly git-ignored.

Scope Management: Minimalist OAuth scopes (typically `drive.file`) are used by default.

Static Analysis: Monitored by \`Bandit to prevent common security pitfalls in API handling.

______________________________________________________________________

**João Pedro** | Automation Engineer
<br />
[GitHub](https://github.com/JoPedro15) • [Automation Hub](https://github.com/JoPedro15/automation-hub) • [AI Lab](https://github.com/JoPedro15/ai-lab)
<br />
