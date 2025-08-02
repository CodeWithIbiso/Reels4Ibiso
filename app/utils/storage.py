import json
from pathlib import Path
from typing import Dict, Any, List

STORAGE_FILE = Path("storage/storage.json")

def read_storage() -> Dict[str, Any]:
    """Read and return data from the storage file.

    Returns:
        A dictionary containing the data from the storage file.
        If the file does not exist, returns an empty dictionary.
    """
    if STORAGE_FILE.exists():
        if STORAGE_FILE.stat().st_size == 0:
            # Initialize with an empty dictionary if the file is empty
            write_storage({})
            return {}
        with open(STORAGE_FILE, "r") as file:
            return json.load(file)
    return {}

def write_storage(data: Dict[str, Any]) -> None:
    """Write data to the storage file.

    Args:
        data: A dictionary containing the data to be written to the storage file.
    """
    with open(STORAGE_FILE, "w") as file:
        json.dump(data, file, indent=4)

def add_upload_record(record: Dict[str, Any]) -> None:
    """Add a new upload record to the storage.

    Args:
        record: A dictionary containing the upload record to be added.
    """
    data = read_storage()
    uploads = data.get("uploads", [])
    uploads.append(record)
    data["uploads"] = uploads
    write_storage(data)

def save_to_storage(uploaded_files_info: List[Dict[str, Any]]) -> None:
    """Save uploaded files information to the storage.

    Args:
        uploaded_files_info: A list of dictionaries containing information about uploaded files.
    """
    data = read_storage()
    uploads = data.get("uploads", [])
    uploads.extend(uploaded_files_info)
    data["uploads"] = uploads
    write_storage(data)

# Example usage
if __name__ == "__main__":
    # Add a new upload record
    new_record = {
        "filename": "example.txt",
        "upload_time": "2023-10-01T12:00:00",
        "description": "Sample file upload"
    }
    add_upload_record(new_record)

    # Read and print all records
    print(read_storage())