"""
Google Docs API service using Service Account authentication.
"""
import os
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Load environment variables
load_dotenv()

class GoogleDocsService:
    def __init__(self):
        self.service = None
        self.authenticate()
    
    def authenticate(self):
        """Authenticate with Google Docs API using Service Account."""
        try:
            creds_path = os.getenv('GOOGLE_CREDENTIALS_PATH')
            if not creds_path:
                raise ValueError("GOOGLE_CREDENTIALS_PATH not found in .env file")
            
            if not os.path.exists(creds_path):
                raise FileNotFoundError(f"Service account key not found at: {creds_path}")

            scopes = [
                'https://www.googleapis.com/auth/documents',
                'https://www.googleapis.com/auth/drive'
            ]
            creds = service_account.Credentials.from_service_account_file(
                creds_path, scopes=scopes)
            
            self.service = build('docs', 'v1', credentials=creds)
            self.drive_service = build('drive', 'v3', credentials=creds)
            print("✅ Successfully authenticated with Google Docs & Drive APIs (Service Account)")
            
        except Exception as e:
            print(f"❌ Authentication failed: {e}")
            raise
    
    def create_document(self, title):
        """Create a new Google Doc using Drive API."""
        try:
            file_metadata = {
                'name': title,
                'mimeType': 'application/vnd.google-apps.document'
            }
            doc = self.drive_service.files().create(body=file_metadata, fields='id').execute()
            doc_id = doc.get('id')
            print(f"✅ Document created: https://docs.google.com/document/d/{doc_id}")
            return doc_id
        except HttpError as error:
            print(f"❌ Error creating document: {error}")
            raise
    
    def format_document(self, doc_id, requests):
        """Apply formatting to a Google Doc."""
        try:
            result = self.service.documents().batchUpdate(
                documentId=doc_id,
                body={'requests': requests}
            ).execute()
            print(f"✅ Document formatted successfully: {result}")
            return result
        except HttpError as error:
            print(f"❌ Error formatting document: {error}")
            raise

    def share_document(self, file_id, email_address, role='writer'):
        """Share the document with a specific email address."""
        try:
            self.drive_service.permissions().create(
                fileId=file_id,
                body={
                    'type': 'user',
                    'role': role,
                    'emailAddress': email_address
                },
                fields='id'
            ).execute()
            print(f"✅ Document shared with {email_address}")
        except HttpError as error:
            print(f"❌ Error sharing document: {error}")
            raise
