from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request

class DriveService:
    SCOPES = ['https://www.googleapis.com/auth/drive']
    SERVICE_ACCOUNT_FILE = '.service_account.json'

    def __init__(self, parent_folder_id):
        """
            Initializes a new instance of the DriveService class.

            Parameters:
                parent_folder_id (str): The ID of the parent folder in Google Drive.

            Returns:
                None
        """

        self.service = self.authenticate()
        self.parent_folder_id = parent_folder_id

    def authenticate(self):
        """
            Authenticates the user and returns a service object for interacting with Google Drive API.

            Returns:
                googleapiclient.discovery.Resource: The service object for interacting with Google Drive API.
        """
        creds = None
        try:
            creds = service_account.Credentials.from_service_account_file(
                self.SERVICE_ACCOUNT_FILE, scopes=self.SCOPES)
            
            if creds.expired:
                creds.refresh(Request())

        except Exception as e:
            print("An error occurred during authentication:", e)

        return build('drive', 'v3', credentials=creds)

        
    def upload_file(self, file_path, file_name):
        """
            Uploads a file to Google Drive and sets public permission.

            Args:
                file_path (str): The path of the file to be uploaded.
                file_name (str): The name of the file to be uploaded.

            Returns:
                str or None: The ID of the uploaded file if successful, None otherwise.

            Raises:
                Exception: If an error occurs during the upload process.

            Note:
                - The `file_path` argument should be the path of the file to be uploaded.
                - The `file_name` argument should be the name of the file to be uploaded.
                - The file will be uploaded to the parent folder specified in `self.parent_folder_id`.
                - If the upload is successful, the ID of the uploaded file will be printed.
                - If an error occurs during the upload process, an error message will be printed.
        """
        file_metadata = {
            'name': file_name,
            'parents': [self.parent_folder_id],
        }

        media = MediaFileUpload(file_path, resumable=True)

        try:
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()
            
            # Set public permission
            self.service.permissions().create(
                fileId=file['id'],
                body={'type': 'anyone', 'role': 'reader'},
            ).execute()
            
            print("File uploaded successfully. File ID:", file.get('id'))
            return file.get('id')
        except Exception as e:
            print("An error occurred:", e)
            return None
        
if __name__ =="__main__":
    parent_folder_id = '1QvD0Mf6GplCMz2DGo66yy80eVPG4gWsN'
    drive_service = DriveService(parent_folder_id)
    drive_service.upload_file(file_path="/home/bhushan/Pictures/pictures/file.jpeg", file_name="Pragati.jpeg")