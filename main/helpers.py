import os

def construct_base_url():
    url_components = {
        "scheme": "https",
        "domain": "api.nasa.gov",
        "path": "neo/rest/v1/feed",
    }
    return url_components

def build_base_url(base_url_components):
    # Construct the base URL
    base_url = f"{base_url_components['scheme']}://{base_url_components['domain']}/{base_url_components['path']}"

    return base_url

BASE_URL = build_base_url(construct_base_url())

def delete_all_files_in_directory(directory_path):
    try:
        # Check if the directory exists
        if not os.path.exists(directory_path):
            print(f"Directory does not exist: {directory_path}")
            return

        # Iterate over the files in the directory
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)

            # Delete files only (skip directories)
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Deleted file: {file_path}")

        print("All files deleted successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
