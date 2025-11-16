# main.py

import os
import time
import socket
import psutil
import ctypes
from getpass import getpass

from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Header, Footer, Button, Static, Input

COMMENTS_FILE = "comments.txt"

# ======================
# WIDGETS
# ======================
class ActiveUsersWidget(Static):
    """Displays currently logged-in users"""
    def __init__(self, app_ref):
        super().__init__()
        self.app_ref = app_ref

    def update_users(self):
        if not self.app_ref.active_users:
            self.update("No active users")
        else:
            self.update("Active Users:\n" + "\n".join(self.app_ref.active_users))

class CommentSectionWidget(Static):
    """Displays comments and allows adding comments"""
    def __init__(self, app_ref):
        super().__init__()
        self.app_ref = app_ref
        self.input_widget = None

    def on_mount(self):
        # Vytvorenie inputu
        self.input_widget = Input(placeholder="Enter comment and press Enter")
        self.input_widget.border_title = "Add Comment"
        self.app_ref.mount(self.input_widget, after=self)
        self.refresh_comments()

    def refresh_comments(self):
        if os.path.exists(COMMENTS_FILE):
            with open(COMMENTS_FILE, "r", encoding="utf-8") as f:
                lines = f.readlines()
        else:
            lines = []

        if not lines:
            self.update("No comments yet.")
        else:
            self.update("\n".join([line.strip() for line in lines]))

    def on_input_submitted(self, message: Input.Submitted):
        if self.app_ref.current_user is None:
            return
        comment = message.value.strip()
        if comment:
            with open(COMMENTS_FILE, "a", encoding="utf-8") as f:
                f.write(f"{self.app_ref.current_user}: {comment}\n")
        message.input.value = ""
        self.refresh_comments()

# ======================
# MAIN APP
# ======================
class PCToolkitApp(App):
    CSS = """
    Screen {
        layout: vertical;
    }
    #main_container {
        height: 1fr;
        layout: horizontal;
    }
    #toolkit_buttons {
        width: 30%;
        padding: 1;
    }
    #comments_area {
        width: 70%;
        padding: 1;
    }
    """

    current_user = None
    active_users = []

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Static("=== P C TOOLKIT PRO v1.0 ===", id="banner")
        with Horizontal(id="main_container"):
            with Vertical(id="toolkit_buttons"):
                yield Button("PC Cleaner", id="pc_cleaner")
                yield Button("System Info", id="system_info")
                yield Button("Network Tools", id="network_tools")
                yield Button("Port Scanner", id="port_scanner")
                yield Button("Fake Error", id="fake_error")
                yield Button("Password Strength", id="password_strength")
                yield Button("File Locker", id="file_locker")
                yield Button("Performance Monitor", id="performance_monitor")
                yield Button("Cheapest Game Finder", id="cheapest_game")
            with Vertical(id="comments_area"):
                self.users_widget = ActiveUsersWidget(self)
                yield self.users_widget
                self.comments_widget = CommentSectionWidget(self)
                yield self.comments_widget
        yield Footer()

    # ======================
    # LOGIN
    # ======================
    def login_user(self):
        if self.current_user is None:
            username = input("Enter your name to login: ").strip()
            if username:
                self.current_user = username
                self.active_users.append(username)
                print(f"Logged in as {username}")

    # ======================
    # BUTTON HANDLERS
    # ======================
    def on_button_pressed(self, event: Button.Pressed):
        label = event.button.label
        if label == "PC Cleaner":
            self.run_pc_cleaner()
        elif label == "System Info":
            self.show_system_info()
        elif label == "Network Tools":
            self.show_network_info()
        elif label == "Port Scanner":
            self.port_scanner()
        elif label == "Fake Error":
            self.fake_error()
        elif label == "Password Strength":
            self.password_strength()
        elif label == "File Locker":
            self.file_locker()
        elif label == "Performance Monitor":
            self.performance_monitor()
        elif label == "Cheapest Game Finder":
            self.cheapest_game_finder()

    # ======================
    # TOOLKIT FUNCTIONS
    # ======================
    def run_pc_cleaner(self):
        temp = os.path.expanduser("~/AppData/Local/Temp")
        deleted = 0
        for root, dirs, files in os.walk(temp):
            for f in files:
                try:
                    os.remove(os.path.join(root, f))
                    deleted += 1
                except:
                    pass
        self.console.print(f"Deleted {deleted} temp files.")

    def show_system_info(self):
        self.console.print(f"CPU Usage: {psutil.cpu_percent()}%")
        self.console.print(f"RAM Usage: {psutil.virtual_memory().percent}%")
        self.console.print(f"Disk Usage: {psutil.disk_usage('/').percent}%")

    def show_network_info(self):
        host = "google.com"
        self.console.print(f"Pinging {host}...")
        os.system(f"ping {host} -n 1")
        self.console.print(f"Local IP: {socket.gethostbyname(socket.gethostname())}")

    def port_scanner(self):
        target = "127.0.0.1"
        ports = [21,22,23,53,80,443,25565]
        for port in ports:
            s = socket.socket()
            s.settimeout(0.5)
            try:
                s.connect((target, port))
                self.console.print(f"[OPEN] {port}")
            except:
                self.console.print(f"[CLOSED] {port}")
            s.close()

    def fake_error(self):
        ctypes.windll.user32.MessageBoxW(0, "Fake Error Triggered!", "System Error", 0x10)

    def password_strength(self):
        pwd = getpass("Enter password for strength check: ")
        score = 0
        if len(pwd) >= 8: score += 1
        if any(c.isupper() for c in pwd): score += 1
        if any(c.isdigit() for c in pwd): score += 1
        if any(c in "!@#$%^&*()-_=+{}" for c in pwd): score += 1
        levels = ["WEAK","OK","GOOD","STRONG","EXTREME"]
        self.console.print(f"Password strength: {levels[score]}")

    def file_locker(self):
        path = input("File or folder path to lock: ").strip()
        if not os.path.exists(path):
            self.console.print("Path does not exist!")
            return
        password = getpass("Set password: ")
        def encrypt_file(file_path):
            try:
                with open(file_path,"rb") as f:
                    data = f.read()
                encrypted = bytearray(b ^ 123 for b in data)
                with open(file_path,"wb") as f:
                    f.write(encrypted)
            except:
                pass
        if os.path.isfile(path):
            encrypt_file(path)
        elif os.path.isdir(path):
            for root, dirs, files in os.walk(path):
                for file in files:
                    encrypt_file(os.path.join(root,file))
        self.console.print("Locking done!")

    def performance_monitor(self):
        try:
            while True:
                self.console.print(f"CPU: {psutil.cpu_percent()}% | RAM: {psutil.virtual_memory().percent}% | Disk: {psutil.disk_usage('/').percent}%")
                time.sleep(1)
        except KeyboardInterrupt:
            pass

    def cheapest_game_finder(self):
        self.console.print("Open marketplaces in browser manually.")

# ======================
# RUN
# ======================
if __name__ == "__main__":
    app = PCToolkitApp()
    app.login_user()
    app.run()
