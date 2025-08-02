# utils/thumbnail.py

from PIL import Image
from pathlib import Path
import subprocess

def generate_thumbnail(file_path: Path) -> str:
    """Generate a thumbnail for an image or video file.

    Args:
        file_path: The path to the file.

    Returns:
        The path to the generated thumbnail.
    """
    thumbnail_dir = file_path.parent / "thumbnails"
    thumbnail_dir.mkdir(exist_ok=True)

    thumbnail_path = thumbnail_dir / f"thumbnail_{file_path.stem}.jpg"

    if file_path.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif']:
        # Handle image files
        with Image.open(file_path) as img:
            img.thumbnail((128, 128))  # Resize image to thumbnail size
            img.save(thumbnail_path)
    elif file_path.suffix.lower() in ['.mp4', '.avi', '.mov', '.mkv']:
        # Handle video files using ffmpeg
        command = [
            'ffmpeg', '-i', str(file_path),
            '-ss', '00:00:01.000', '-vframes', '1',
            str(thumbnail_path)
        ]
        subprocess.run(command, check=True)

    return str(thumbnail_path)