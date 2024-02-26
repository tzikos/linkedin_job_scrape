from googleapiclient.discovery import build
from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = '/Users/tzikos/Downloads/general-use-415421-e34fd089dc23.json'
PARENT_FOLDER_ID='1SobdmvtfHBRTAf9I1bTkQZaMMvv8aFwJ'

def authenticate():
    creds=service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return creds

def upload(file_path):
    creds=authenticate()
    service=build('drive','v3',credentials=creds)

    file_metadata= {
        'name': 'Data.csv',
        'parents': [PARENT_FOLDER_ID]
    }

    file = service.files().create(
        body=file_metadata,
        media_body=file_path
    ).execute()

upload('/Users/tzikos/Desktop/python tasks/linkedin_job_scrape/expo/FOR_GOOGLE_DRIVE/DATA_FOR_GDRIVE.csv')