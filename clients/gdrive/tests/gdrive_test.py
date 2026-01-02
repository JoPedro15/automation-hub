# ruff: noqa: S101
import os
import time
from pathlib import Path

import pytest
from dotenv import load_dotenv

from clients.gdrive import GDriveClient


@pytest.fixture(scope="module")
def gdrive_setup() -> tuple[GDriveClient, str]:
    """
    Setup client and target folder for integration tests.
    Ensures environment variables are present before starting.
    """
    load_dotenv()
    root: Path = Path(__file__).parent.parent
    creds: str = str(root / "data" / "credentials.json")
    token: str = str(root / "data" / "token.json")
    folder_id: str = os.getenv("OUTPUT_FOLDER_ID", "")

    if not folder_id:
        pytest.skip("OUTPUT_FOLDER_ID not set, skipping integration tests.")

    client: GDriveClient = GDriveClient(creds, token)
    return client, folder_id


def test_gdrive_full_lifecycle(gdrive_setup: tuple[GDriveClient, str]) -> None:
    """
    Tests the full CRUD lifecycle of files in Google Drive.

    Steps:
    1. Upload test_1.txt
    2. Check existence
    3. Upload multiple files (test_2, test_3)
    4. Delete specific file
    5. Clear entire folder
    6. Verify empty state
    """
    client, folder_id = gdrive_setup
    local_test_files: list[str] = ["test_1.txt", "test_2.txt", "test_3.txt"]

    try:
        # Pre-test cleanup to ensure isolation
        client.clear_folder_content(folder_id)

        # --- TEST 1: Create/Upload test_1.txt ---
        file_name_1: str = local_test_files[0]
        with open(file_name_1, "w") as f:
            f.write("Automation test content")

        file_id_1: str = client.upload_file(file_name_1, folder_id)
        assert file_id_1 is not None

        # --- TEST 2: Validate existence ---
        assert client.file_exists(file_name_1, folder_id) is True

        # --- TEST 3: Add multiple files ---
        for name in local_test_files[1:]:
            with open(name, "w") as f:
                f.write(f"Content for {name}")
            client.upload_file(name, folder_id)

        # Small sleep to account for API propagation
        time.sleep(1)

        files_list: list = client.list_files(folder_id)
        assert len(files_list) == 3

        # --- TEST 4: Delete specific file ---
        client.delete_specific_file("test_3.txt", folder_id)
        time.sleep(1)  # API propagation
        assert client.file_exists("test_3.txt", folder_id) is False
        assert len(client.list_files(folder_id)) == 2

        # --- TEST 5 & 6: Clear all and validate ---
        client.clear_folder_content(folder_id)
        time.sleep(1)  # API propagation
        assert len(client.list_files(folder_id)) == 0

    finally:
        # Cleanup local artifacts even if assertions fail
        for file_name in local_test_files:
            file_path = Path(file_name)
            if file_path.exists():
                file_path.unlink()
