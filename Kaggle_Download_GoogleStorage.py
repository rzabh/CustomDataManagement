import os
import requests
from directory_utils import clear_directory




# URL for images_001.zip
# Right Click on your desired Kaggle directory on any other type of url
file_url = "https://storage.googleapis.com/kaggle-data-sets/5839/18613/upload/images_001.zip?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=gcp-kaggle-com%40kaggle-161607.iam.gserviceaccount.com%2F20241110%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20241110T133030Z&X-Goog-Expires=259200&X-Goog-SignedHeaders=host&X-Goog-Signature=82ed012fc8a5d8d339b9854e637874e01d94a177242afd9a13c7bbec08840b7e71e3fb6806e4c2d6cc23ffa9afc50086602353d47edbe48592739ee2e9c03c3c9d90ae902178d61a5d269804d14203596f09359006b70f87909b5164df8e842d58e481a5a9b32226ce94dc56348b03db33df4b93d7b5d8d640e387f037f2c64bbea5ecd9ecd596ed56c0be8c87e0e21c9755d2f83c1bc211fd5cde359fdf9c6cd94c3ef9c0476ed7c8d5ff5687e1c739147b8682bd92d3f11d647b2aabaa7d85e99aff713e6d7c0689ab2c21ca20c8c3739d3fd1cbdc3e160d388c8720d9b732055cc4866320a484ce8b5e0d7f61a5aea3bae4093920875b70cbaa28695c18a8"

# Output directory and file path
output_directory = "kaggle_directory"
#clear_directory("kaggle_directory", remove_folders=True)

os.makedirs(output_directory, exist_ok=True)  # Ensure directory exists
output_file = os.path.join(output_directory, "images_001.zip")

# Download the file with progress
try:
    print(f"Downloading {output_file}...")
    response = requests.get(file_url, stream=True)
    response.raise_for_status()  # Check for HTTP errors

    # Get total file size from headers
    total_size = int(response.headers.get('content-length', 0))
    downloaded_size = 0

    with open(output_file, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):  # Stream content in chunks
            if chunk:  # Filter out keep-alive new chunks
                f.write(chunk)
                downloaded_size += len(chunk)

                # Calculate and display progress
                progress = (downloaded_size / total_size) * 100 if total_size > 0 else 0
                print(f"\rProgress: {progress:.2f}% ({downloaded_size}/{total_size} bytes)", end="")

    print(f"\nDownload complete: {output_file}")
except requests.RequestException as e:
    print(f"Error downloading file: {e}")
