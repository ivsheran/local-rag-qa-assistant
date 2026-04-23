from google.oauth2 import service_account
from googleapiclient.discovery import build
import io
from googleapiclient.http import MediaIoBaseDownload

class DriveClient:
    def __init__(self, credentials_path, scopes=['https://www.googleapis.com/auth/drive.readonly']):
        self.credentials = service_account.Credentials.from_service_account_file(credentials_path, scopes=scopes)
        self.service = build('drive', 'v3', credentials=self.credentials)

    def list_files_in_folder(self, folder_id):
        query = f"'{folder_id}' in parents"
        
        results = self.service.files().list(q=query, fields="files(id, name, mimeType, modifiedTime)").execute()
        return results.get('files', [])

    def download_file(self, file_id, mime_type=None):
        request = self.service.files().get_media(fileId=file_id)
        file_data = io.BytesIO()
        downloader = MediaIoBaseDownload(file_data, request)

        done = False
        while not done:
            status, done = downloader.next_chunk()

        file_data.seek(0)
        return file_data