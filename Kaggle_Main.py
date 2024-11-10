import os
from kaggle.api.kaggle_api_extended import KaggleApi
import time
from directory_utils import clear_directory

# Set up Kaggle credentials
# On the Kaggle website, go to Settings → API → Create New Token.
# Save the JSON file to the .kaggle folder in C:\Users\[YourUsername]\.kaggle.
os.environ['KAGGLE_USERNAME'] = ""  # Replace with your Kaggle username
os.environ['KAGGLE_KEY'] = ""  # Replace with your actual Kaggle API key

# Define dataset and version
dataset = "nih-chest-xrays/data"  # Target dataset
kaggle_directory = "kaggle_directory"
os.makedirs(kaggle_directory, exist_ok=True)
clear_directory("kaggle_directory", remove_folders=True)


# Create output folder for selected files
base_output_dir = os.path.join(kaggle_directory, "nih-chest-xrays-images")
os.makedirs(base_output_dir, exist_ok=True)

# Authenticate Kaggle API
api = KaggleApi()
api.authenticate()

# Target subdirectory to download files from (e.g., "images_001")
target_directory = "images_001"  # Replace with the specific subdirectory you need

# List files in the dataset
files = api.dataset_list_files(dataset).files
print(f"Found {len(files)} top-level files in the dataset (version 3).")

# Filter files that belong to the target directory
target_files = [file for file in files if file.name.startswith(target_directory)]
print(f"Found {len(target_files)} files in the target directory '{target_directory}'.")

if len(target_files) == 0:
    print(f"No files found in the target directory '{target_directory}'. Exiting...")
    exit()

# Batch size for downloading
batch_size = 10  # Adjust to download fewer files per batch
for i in range(0, len(target_files), batch_size):
    batch = target_files[i:i + batch_size]
    print(f"\nProcessing batch {i // batch_size + 1} with {len(batch)} files...")

    for file in batch:
        try:
            # Create output folder structure
            subfolder = os.path.dirname(file.name)
            output_dir = os.path.join(base_output_dir, subfolder)
            os.makedirs(output_dir, exist_ok=True)

            # Check if the file already exists
            local_file_path = os.path.join(output_dir, os.path.basename(file.name))
            if os.path.exists(local_file_path):
                print(f"File already exists: {local_file_path}. Skipping download.")
                continue

            # Download the file
            print(f"Downloading {file.name} to {output_dir}...")
            api.dataset_download_file(dataset, file_name=file.name, path=output_dir)
            print(f"Downloaded: {file.name} to {output_dir}")
        except Exception as e:
            print(f"Error downloading {file.name}: {e}")

    # Pause between batches to avoid rate limits
    print(f"Batch {i // batch_size + 1} completed. Pausing before next batch...")
    time.sleep(1)  # Adjust pause duration if needed


# List all files in the dataset
print("Fetching dataset files...")
try:
    files = api.dataset_list_files(dataset).files
    print(f"Found {len(files)} files in the dataset.")
except Exception as e:
    print(f"Error fetching dataset files: {e}")
    exit()

# Filter out image files
image_extensions = (".png", ".jpg", ".jpeg")
non_image_files = [file for file in files if not file.name.endswith(image_extensions)]
print(f"Found {len(non_image_files)} non-image files in the dataset.")

if not non_image_files:
    print("No non-image files found in the dataset. Exiting...")
    exit()

# Download each non-image file
for file in non_image_files:
    try:
        print(f"Downloading '{file.name}'...")
        api.dataset_download_file(dataset, file_name=file.name, path=kaggle_directory)
        print(f"'{file.name}' downloaded successfully to '{output_dir}'")
    except Exception as e:
        print(f"Error downloading '{file.name}': {e}")