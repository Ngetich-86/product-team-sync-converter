"""
Google Docs API client for creating and formatting documents.
"""
try:
    from google.colab import auth
except ImportError:
    auth = None
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class GoogleDocsClient:
    def __init__(self):
        self.service = None
        self.authenticate()
    
    def authenticate(self):
        """Authenticate with Google Docs API in Colab environment."""
        try:
            auth.authenticate_user()
            self.service = build('docs', 'v1')
            print("✅ Successfully authenticated with Google Docs API")
        except Exception as e:
            print(f"❌ Authentication failed: {e}")
            raise
    
    def create_document(self, title):
        """Create a new Google Doc."""
        try:
            document = self.service.documents().create(body={'title': title}).execute()
            doc_id = document.get('documentId')
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