# Alt-Drag & Resize Tool for Windows

It's the feature from Linux Mint Cinnamon. AI summary of AI made tool (of course at my direction as far as I can direct it fwiw) follows - This tool brings a popular Linux window management feature to Windows. It allows you to move and resize windows without having to find the title bar or corners.

## How to use:

- **Move a window:** Hold the `Alt` key and **Left-Click + Drag** anywhere inside a window.
- **Resize a window:** Hold the `Alt` key and **Right-Click + Drag** anywhere inside a window.
  - Clicking in the top-left quadrant will drag the top-left corner.
  - Clicking in the bottom-right quadrant will drag the bottom-right corner.
  - ... and so on for all 4 corners/sides.
- **Exit:** Press `Alt + Shift + Q` or close the command window.

## Installation:

1. Make sure you have Python installed.
2. Install dependencies:
   ```bash
   pip install pynput pywin32 winshell pystray Pillow
   ```
3. Run the script:
   ```bash
   python main.py
   ```
   (Or use `run.bat` to launch it in the background without a console window).

## How it works:
- **Background Mode**: When you run the tool, a dialog box with instructions will appear. Once you close it, the tool continues running in the **system tray** (look for a blue icon with a white square).
- **System Tray**: Right-click the tray icon to see instructions again or to exit the tool.

To make the tool run automatically when you log in:
1. Run the `add_to_startup.py` script:
   ```bash
   python add_to_startup.py
   ```
   This creates a shortcut in your Windows Startup folder.

## Troubleshooting:

- **Admin Windows:** To move/resize windows running as Administrator (like Task Manager), you must run this tool as Administrator as well.
- **Maximized Windows:** If you try to move or resize a maximized window, it will automatically be restored to its normal size first.
