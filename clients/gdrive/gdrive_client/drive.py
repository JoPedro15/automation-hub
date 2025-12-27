import os
from typing import Any
from typing import List, Optional, Dict

from googleapiclient.discovery import build, Resource

from clients.gdrive.gdrive_client.auth import get_google_service_credentials


class GDriveClient:
    """
    Client to interact with Google Drive API for automation tasks.
    """

    def __init__(self, credentials_path: str, token_path: str) -> None:
        """
        Initializes the GDriveClient with necessary paths and authenticates.

        :param credentials_path: Path to the credentials.json file.
        :param token_path: Path to the token.json file.
        """
        self.credentials_path: str = credentials_path
        self.token_path: str = token_path
        self.scopes: List[str] = ["https://www.googleapis.com/auth/drive"]

        self.output_folder_id: Optional[str] = os.getenv("OUTPUT_FOLDER_ID")

        self.service: Resource = self._init_service()

    def _init_service(self) -> Resource:
        """
        Internal method to build the Google Drive service resource.

        :return: A Resource object for the Google Drive API.
        """
        creds = get_google_service_credentials(
            self.credentials_path, self.token_path, self.scopes
        )
        return build("drive", "v3", credentials=creds)

    def upload_file(self, file_path: str, folder_id: Optional[str] = None) -> str:
        """
        Uploads a file to a specific Google Drive folder.

        :param file_path: Local path of the file to upload.
        :param folder_id: ID of the folder where the file will be stored.
        :return: The ID of the uploaded file.
        """
        from googleapiclient.http import MediaFileUpload

        file_name: str = os.path.basename(file_path)
        target_folder: str = folder_id or self.output_folder_id or ""

        file_metadata: Dict[str, Any] = {
            "name": file_name,
            "parents": [target_folder] if target_folder else [],
        }

        media: MediaFileUpload = MediaFileUpload(file_path, resumable=True)

        file: Dict[str, Any] = (
            self.service.files()
            .create(body=file_metadata, media_body=media, fields="id")
            .execute()
        )

        print(f"✅ File {file_name} uploaded successfully with ID: {file.get('id')}")
        return str(file.get("id"))

    def clean_folder(
            self, folder_id: str, file_prefix: Optional[str] = None
    ) -> List[str]:
        """
        Deletes files within a specific Google Drive folder based on a prefix.

        :param folder_id: The ID of the folder to clean.
        :param file_prefix: Optional prefix to filter files (e.g., 'test_').
        :return: A list of deleted file IDs.
        """
        if not folder_id:
            print("⚠️ No folder_id provided for cleanup.")
            return []

        # Query construction: files in folder, not in trash
        query: str = f"'{folder_id}' in parents and trashed = false"
        if file_prefix:
            query += f" and name contains '{file_prefix}'"

        results: Dict[str, Any] = (
            self.service.files().list(q=query, fields="files(id, name)").execute()
        )

        files: List[Dict[str, Any]] = results.get("files", [])
        deleted_ids: List[str] = []

        for file in files:
            file_id: str = file["id"]
            self.service.files().delete(fileId=file_id).execute()
            deleted_ids.append(file_id)
            print(f"✅ Deleted: {file['name']} from folder {folder_id}")

        return deleted_ids
