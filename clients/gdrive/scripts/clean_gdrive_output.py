import os
from pathlib import Path
from typing import List

from clients.gdrive.gdrive_client.client import GDriveClient
from dotenv import load_dotenv


def main() -> None:
    """
    Orchestrates the cleanup process of the Google Drive output folder.

    This script initializes the GDrive environment and performs a targeted
    deletion of temporary files using a specific naming convention.
    """
    # Load environment variables (API Keys, Folder IDs, etc.)
    load_dotenv()

    # Define paths using pathlib for robust cross-platform execution (Mac/Linux)
    root: Path = Path(__file__).parent.parent
    creds_path: str = str(root / "data" / "credentials.json")
    token_path: str = str(root / "data" / "token.json")

    # Safety Check: Ensure the target folder ID is present
    output_id: str = os.getenv("OUTPUT_FOLDER_ID", "")

    if not output_id:
        print("❌ Error: OUTPUT_FOLDER_ID not found in environment variables.")
        return

    # Initialize the GDriveClient with the refactored architecture
    client: GDriveClient = GDriveClient(
        credentials_path=creds_path, token_path=token_path
    )

    print(f"🧹 Starting cleanup in folder: {output_id}")
    print("🔍 Filtering files with prefix: 'test_'")

    # The client now handles pagination internally via _fetch_files
    # This call is significantly more performant and reliable
    deleted_ids: List[str] = client.delete_files_by_prefix(
        folder_id=output_id, file_prefix="test_"
    )

    # Final Execution Report
    if deleted_ids:
        print(f"✨ Success! Permanently removed {len(deleted_ids)} items.")
    else:
        print("ℹ️ No files matching the prefix 'test_' were found. Folder is clean.")


if __name__ == "__main__":
    main()
