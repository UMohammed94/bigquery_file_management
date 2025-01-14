from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth import default
import os

def upload_directory_to_drive(local_directory, folder_name):
    """
    Upload all contents from a given directory to a Google Drive folder using login-based auth.
    Args:
        local_directory (str): Path to the local directory to upload.
        folder_name (str): The name of the folder on Google Drive to upload to.
    """
    # Authenticate using gcloud login
    credentials, project = default()
    service = build('drive', 'v3', credentials=credentials)

    # Check if the folder exists; create it if not
    folder_id = None
    query = f"mimeType='application/vnd.google-apps.folder' and trashed=false and name='{folder_name}'"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    items = results.get('files', [])

    if items:
        folder_id = items[0]['id']
        print(f"Folder '{folder_name}' found with ID: {folder_id}")
    else:
        print(f"Folder '{folder_name}' not found. Creating it.")
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        folder = service.files().create(body=file_metadata, fields='id').execute()
        folder_id = folder.get('id')
        print(f"Created folder '{folder_name}' with ID: {folder_id}")

    # Upload files to the folder
    for filename in os.listdir(local_directory):
        file_path = os.path.join(local_directory, filename)

        # Skip directories, only process files
        if os.path.isfile(file_path):
            file_metadata = {'name': filename, 'parents': [folder_id]}
            media = MediaFileUpload(file_path)
            try:
                uploaded_file = service.files().create(
                    body=file_metadata, media_body=media, fields='id'
                ).execute()
                print(f"Uploaded: {filename} (ID: {uploaded_file.get('id')})")
            except Exception as e:
                print(f"Failed to upload {filename}: {e}")

    print("Upload process complete.")

# Example usage
directory_to_upload = "/path/to/your/local/directory"
upload_directory_to_drive(directory_to_upload, "backup")
