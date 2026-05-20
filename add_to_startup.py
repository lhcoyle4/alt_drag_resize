import os
import winshell
from win32com.client import Dispatch

def create_startup_shortcut():
    # Paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    target = os.path.join(current_dir, "run.bat")
    startup_path = winshell.startup()
    shortcut_path = os.path.join(startup_path, "AltDragResize.lnk")

    # Create Shortcut
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(shortcut_path)
    shortcut.Targetpath = target
    shortcut.WorkingDirectory = current_dir
    shortcut.IconLocation = target
    shortcut.Description = "Alt-Drag and Resize Tool"
    shortcut.save()

    print(f"Shortcut created in Startup folder: {shortcut_path}")
    print("The tool will now run automatically when you log in.")

if __name__ == "__main__":
    # Ensure winshell is installed for easier path handling
    try:
        import winshell
    except ImportError:
        import subprocess
        subprocess.check_call(["pip", "install", "winshell"])
        import winshell
        
    create_startup_shortcut()
