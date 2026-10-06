import os
import shutil
import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Define file categories and their extensions
CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".xls", ".pptx", ".csv", ".md"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv"],
    "Audio": [".mp3", ".wav", ".aac", ".flac", ".ogg"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Installers": [".exe", ".msi", ".apk"],
    "Code": [".py", ".html", ".css", ".js", ".cpp", ".c", ".java", ".json"]
}

# Invert dictionary for fast lookup
EXT_TO_DIR = {ext: category for category, exts in CATEGORIES.items() for ext in exts}

def get_target_dir(file_path):
    ext = file_path.suffix.lower()
    return EXT_TO_DIR.get(ext, "Others")

class ClutterHandler(FileSystemEventHandler):
    def __init__(self, watch_dir):
        self.watch_dir = Path(watch_dir)
        super().__init__()

    def on_modified(self, event):
        # We only care about files
        if event.is_directory:
            return
            
        file_path = Path(event.src_path)
        
        # Give the file a second to finish downloading/copying
        time.sleep(1)
        
        self.sort_file(file_path)

    def on_created(self, event):
        if event.is_directory: return
        time.sleep(1)
        self.sort_file(Path(event.src_path))

    def sort_file(self, file_path):
        if not file_path.exists():
            return
            
        # Ignore files that are already inside a sorted category folder
        if file_path.parent != self.watch_dir:
            return
            
        # Ignore partial downloads and shortcuts
        if file_path.suffix.lower() in [".crdownload", ".tmp", ".lnk", ".url", ".ini"]:
            return

        target_folder_name = get_target_dir(file_path)
        
        # Move unknown files to "Others" folder so the directory is completely clean
        if target_folder_name == "Others":
            if file_path.name.lower() == "desktop.ini":
                return
            
        target_dir = self.watch_dir / target_folder_name
        
        try:
            target_dir.mkdir(exist_ok=True)
            
            # Handle filename collisions
            dest_path = target_dir / file_path.name
            counter = 1
            while dest_path.exists():
                dest_path = target_dir / f"{file_path.stem}_{counter}{file_path.suffix}"
                counter += 1
                
            try:
                print(f"Moving: {file_path.name} -> {target_folder_name}/")
            except:
                pass # Ignore unicode print errors
            shutil.move(str(file_path), str(dest_path))
        except Exception as e:
            pass # Suppress background errors

def organize_existing_files(directory):
    path = Path(directory)
    print(f"Scanning existing files in {path}...")
    for item in path.iterdir():
        if item.is_file():
            handler = ClutterHandler(path)
            handler.sort_file(item)

if __name__ == "__main__":
    home = Path.home()
    downloads_dir = home / "Downloads"
    desktop_dir = home / "Desktop"

    # 1. Organize existing files first
    organize_existing_files(downloads_dir)
    # organize_existing_files(desktop_dir) # Only do downloads for now to be safe with Desktop

    # 2. Watch for new files
    observer = Observer()
    
    # Watch Downloads
    if downloads_dir.exists():
        observer.schedule(ClutterHandler(downloads_dir), str(downloads_dir), recursive=False)
        print(f"Watching: {downloads_dir}")
        
    # Watch Desktop
    if desktop_dir.exists():
        observer.schedule(ClutterHandler(desktop_dir), str(desktop_dir), recursive=False)
        print(f"Watching: {desktop_dir}")

    observer.start()
    print("Zero-Clutter is running in the background. Press Ctrl+C to stop.")
    
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
