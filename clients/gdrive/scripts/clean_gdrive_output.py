import os
from pathlib import Path

from clients.gdrive.gdrive_client.drive import GDriveClient
from dotenv import load_dotenv


def main() -> None:
    load_dotenv()

    root: Path = Path(__file__).parent.parent
    creds: str = str(root / "data" / "credentials.json")
    token: str = str(root / "data" / "token.json")

    client: GDriveClient = GDriveClient(credentials_path=creds, token_path=token)

    output_id: str = os.getenv("OUTPUT_FOLDER_ID", "")

    print(f"🧹 Cleaning output folder: {output_id}")
    deleted = client.clean_folder(folder_id=output_id, file_prefix="test_")

    print(f"✨ Done! Removed {len(deleted)} items.")


if __name__ == "__main__":
    main()
