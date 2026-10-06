# Desktop Super Tools 🛠️

A collection of lightweight, powerful background productivity tools for Windows built in Python. These scripts run silently in the background or system tray to automate daily annoyances and speed up your workflow.

## 1. Zero-Clutter File Organizer (`zero_clutter.py`)
Tired of a messy `Downloads` folder? Zero-Clutter is a watchdog script that runs silently in the background and monitors your file system in real-time.

**Features:**
- **Instant Sorting:** The moment you download or save a file, it is automatically moved into organized subfolders (e.g., `Images/`, `Documents/`, `Installers/`).
- **Smart Fallback:** Unrecognized files or obscure extensions are swept into an `Others/` folder, ensuring the root directory remains 100% clean.
- **Collision Handling:** Automatically renames duplicate downloads (e.g., `file_1.pdf`) instead of throwing errors.

## 2. Quick-Drop Notepad (`quick_drop.py`)
A fast, global overlay notepad inspired by dropdown terminals (like Quake). 

**Features:**
- **Global Hotkey:** Press `Ctrl + Shift + Space` from *anywhere* in Windows, no matter what application you have open.
- **Sleek UI:** A translucent, dark-mode, borderless notepad smoothly animates down from the top of your screen.
- **Auto-Save:** Everything you type is instantly saved to disk. You can dismiss the notepad by pressing `Esc` and bring it back later with your notes intact.
- **Focus:** Prevents you from having to minimize your work or open heavy text editors just to jot down a quick phone number or thought.

## 🛠️ Requirements
- **OS:** Windows 10/11
- **Python:** Python 3.8+
- **Dependencies:**
  ```bash
  pip install watchdog pynput PyQt5
  ```

## 🚀 Setup & Installation
1. Clone this repository.
2. Install the required Python packages.
3. Run the scripts in the background using `pythonw` (Windows GUI Python) so they don't leave console windows open:
   ```bash
   pythonw zero_clutter.py
   pythonw quick_drop.py
   ```
4. *(Optional)* Create shortcuts to these scripts and place them in your `shell:startup` folder so they run automatically when you boot your PC.
