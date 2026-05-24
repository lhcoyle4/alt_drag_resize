import win32gui
import win32api
import win32con
from pynput import mouse, keyboard
import sys
import os
import threading
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageDraw
import pystray

class AltDragTool:
    def __init__(self):
        self.alt_pressed = False
        self.ctrl_pressed = False
        self.dragging = False
        self.resizing = False
        self.target_hwnd = None
        self.start_mouse_pos = (0, 0)
        self.start_window_rect = (0, 0, 0, 0)
        self.resize_edges = (False, False, False, False)
        self.running = True
        self.icon = None

    def get_window_under_mouse(self):
        pos = win32api.GetCursorPos()
        hwnd = win32gui.WindowFromPoint(pos)
        if hwnd:
            return win32gui.GetAncestor(hwnd, win32con.GA_ROOT)
        return None

    def on_key_press(self, key):
        if key in [keyboard.Key.alt, keyboard.Key.alt_l, keyboard.Key.alt_r]:
            self.alt_pressed = True
        elif key in [keyboard.Key.ctrl, keyboard.Key.ctrl_l, keyboard.Key.ctrl_r]:
            self.ctrl_pressed = True
        elif hasattr(key, 'char') and key.char == 'q':
            if self.alt_pressed and self.ctrl_pressed:
                hwnd = self.get_window_under_mouse()
                if hwnd:
                    class_name = win32gui.GetClassName(hwnd)
                    if class_name not in ["Shell_TrayWnd", "WorkerW", "Progman"]:
                        win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)

    def on_key_release(self, key):
        if key in [keyboard.Key.alt, keyboard.Key.alt_l, keyboard.Key.alt_r]:
            self.alt_pressed = False
        elif key in [keyboard.Key.ctrl, keyboard.Key.ctrl_l, keyboard.Key.ctrl_r]:
            self.ctrl_pressed = False

    def on_click(self, x, y, button, pressed):
        if self.alt_pressed and pressed:
            hwnd = self.get_window_under_mouse()
            if not hwnd: return
            class_name = win32gui.GetClassName(hwnd)
            if class_name in ["Shell_TrayWnd", "WorkerW", "Progman"]: return

            self.target_hwnd = hwnd
            self.start_mouse_pos = (x, y)
            if win32gui.GetWindowPlacement(self.target_hwnd)[1] == win32con.SW_SHOWMAXIMIZED:
                win32gui.ShowWindow(self.target_hwnd, win32con.SW_RESTORE)
            self.start_window_rect = win32gui.GetWindowRect(self.target_hwnd)
            
            if button == mouse.Button.left:
                self.dragging, self.resizing = True, False
            elif button == mouse.Button.right:
                self.resizing, self.dragging = True, False
                l, t, r, b = self.start_window_rect
                w, h = r - l, b - t
                rel_x, rel_y = x - l, y - t
                self.resize_edges = (rel_x < w/2, rel_y < h/2, rel_x >= w/2, rel_y >= h/2)
            
            win32gui.SendMessage(self.target_hwnd, win32con.WM_CANCELMODE, 0, 0)

        if not pressed:
            self.dragging = False
            self.resizing = False
            self.target_hwnd = None

    def on_move(self, x, y):
        if not self.target_hwnd: return
        dx, dy = x - self.start_mouse_pos[0], y - self.start_mouse_pos[1]
        if self.dragging:
            l, t, r, b = self.start_window_rect
            win32gui.MoveWindow(self.target_hwnd, l + dx, t + dy, r - l, b - t, True)
        elif self.resizing:
            l, t, r, b = self.start_window_rect
            nl, nt, nr, nb = l, t, r, b
            if self.resize_edges[0]: nl += dx
            if self.resize_edges[1]: nt += dy
            if self.resize_edges[2]: nr += dx
            if self.resize_edges[3]: nb += dy
            if nr - nl < 150:
                if self.resize_edges[0]: nl = nr - 150
                else: nr = nl + 150
            if nb - nt < 100:
                if self.resize_edges[1]: nt = nb - 100
                else: nb = nt + 100
            win32gui.MoveWindow(self.target_hwnd, nl, nt, nr - nl, nb - nt, True)

    def create_image(self):
        # Generate a simple blue icon with a white 'A'
        image = Image.new('RGB', (64, 64), color=(0, 120, 215))
        dc = ImageDraw.Draw(image)
        dc.rectangle((16, 16, 48, 48), fill=(255, 255, 255))
        return image

    def show_instructions(self):
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo("Alt-Drag Tool Instructions", 
            "Alt-Drag Tool is running!\n\n"
            "• Hold ALT + Left Click to MOVE windows.\n"
            "• Hold ALT + Right Click to RESIZE windows.\n"
            "• Press CTRL + ALT + Q to CLOSE the window under your mouse.\n\n"
            "The tool is now in your system tray.")
        root.destroy()

    def quit_app(self, icon, item):
        self.running = False
        self.icon.stop()
        os._exit(0)

    def run(self):
        # Tray Icon setup
        self.icon = pystray.Icon("AltDrag", self.create_image(), "Alt-Drag Tool", menu=pystray.Menu(
            pystray.MenuItem("Instructions", lambda: threading.Thread(target=self.show_instructions, daemon=True).start()),
            pystray.MenuItem("Exit", self.quit_app)
        ))

        # Input Listeners
        m_listener = mouse.Listener(on_click=self.on_click, on_move=self.on_move)
        k_listener = keyboard.Listener(on_press=self.on_key_press, on_release=self.on_key_release)
        
        m_listener.start()
        k_listener.start()
        
        self.icon.run() # This is a blocking call

if __name__ == "__main__":
    tool = AltDragTool()
    tool.run()
