import os
import time
import requests
import webbrowser
import psutil
import socket
import ctypes
from getpass import getpass
import threading

# ======================
# COLORS
# ======================
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BLUE = "\033[94m"
RESET = "\033[0m"

# ======================
# UTILITY FUNCTIONS
# ======================
def clear():
    os.system("cls" if os.name == "nt" else "clear")

# ======================
# STARTUP - BANNER
# ======================
def show_intro():
    clear()
    banner = f"""
{BLUE}========================================
      P C   T O O L K I T   P R O
                 v1.0
========================================{RESET}
"""
    print(banner)
    print(f"{CYAN}Welcome to PC Toolkit!{RESET}\n")
    time.sleep(3)  # krátka pauza na prečítanie

# ======================
# PC CLEANER
# ======================
def safe_delete_in_folder(folder, extensions=None):
    deleted = 0
    folder = os.path.expandvars(os.path.expanduser(folder))
    if not os.path.exists(folder):
        print(f"[X] Folder not found: {folder}")
        return 0
    for root, dirs, files in os.walk(folder):
        for f in files:
            if extensions is None or f.lower().endswith(extensions):
                try:
                    os.remove(os.path.join(root, f))
                    deleted += 1
                except:
                    pass
    print(f"[✔] Deleted {deleted} files from {folder}")
    return deleted

def pc_cleaner():
    clear()
    print(f"{CYAN}=== PC CLEANER ==={RESET}\n")
    print("1 - Clean Temp Files")
    print("2 - Clean Downloads")
    print("3 - Photo Cleaner (jpg, png)")
    print("4 - MP3 Cleaner")
    print("5 - MP4 Cleaner")
    print("6 - Full Clean (Temp + Photos + MP3 + MP4)")
    print("0 - Back")

    choice = input("Choose: ")

    downloads = os.path.expanduser("~/Downloads")
    pictures = os.path.expanduser("~/Pictures")
    music = os.path.expanduser("~/Music")
    videos = os.path.expanduser("~/Videos")
    temp = os.path.expanduser("~/AppData/Local/Temp")

    def freeze_warning():
        print("\n[!] If the program appears stuck while deleting files, check your taskbar.\n")

    if choice in ["3","4","5","6"]:
        t = threading.Timer(5.0, freeze_warning)
        t.start()

    if choice == "1":
        safe_delete_in_folder(temp)
    elif choice == "2":
        safe_delete_in_folder(downloads)
    elif choice == "3":
        safe_delete_in_folder(pictures, (".jpg", ".jpeg", ".png"))
    elif choice == "4":
        safe_delete_in_folder(music, (".mp3",))
    elif choice == "5":
        safe_delete_in_folder(videos, (".mp4",))
    elif choice == "6":
        safe_delete_in_folder(temp)
        safe_delete_in_folder(downloads)
        safe_delete_in_folder(pictures, (".jpg", ".jpeg", ".png"))
        safe_delete_in_folder(music, (".mp3",))
        safe_delete_in_folder(videos, (".mp4",))
    else:
        print(f"{YELLOW}Back to menu...{RESET}")

    if choice in ["3","4","5","6"]:
        t.cancel()

    input("\nPress ENTER to return to menu...")

# ======================
# SYSTEM INFO
# ======================
def system_info():
    clear()
    print(f"{CYAN}=== SYSTEM INFO ==={RESET}\n")
    print("CPU Usage:", psutil.cpu_percent(interval=1), "%")
    print("RAM Usage:", psutil.virtual_memory().percent, "%")
    print("Disk Usage:", psutil.disk_usage('/').percent, "%")
    input("\nPress ENTER to return to menu...")

# ======================
# NETWORK TOOLS
# ======================
def network_tools():
    clear()
    print(f"{CYAN}=== NETWORK TOOLS ==={RESET}\n")
    host = input("Ping host (e.g., google.com): ").strip()
    if host != "":
        os.system(f"ping {host}")
    print("Local IP:", socket.gethostbyname(socket.gethostname()))
    input("\nPress ENTER to return to menu...")

# ======================
# PORT SCANNER
# ======================
def port_scanner():
    clear()
    print(f"{CYAN}=== PORT SCANNER ==={RESET}\n")
    target = input("Target IP: ").strip()
    ports = [21,22,23,53,80,443,25565]
    print(f"\nScanning {target}...\n")
    for port in ports:
        s = socket.socket()
        s.settimeout(0.5)
        try:
            s.connect((target, port))
            print(f"{GREEN}OPEN:{RESET} {port}")
        except:
            print(f"{RED}CLOSED:{RESET} {port}")
        s.close()
    input("\nPress ENTER to return to menu...")

# ======================
# FAKE ERROR MESSAGE
# ======================
def fake_error():
    clear()
    print(f"{CYAN}=== FAKE ERROR ==={RESET}\n")
    msg = input("Error message text: ")
    ctypes.windll.user32.MessageBoxW(0, msg, "System Error", 0x10)
    print(f"{GREEN}Error displayed!{RESET}")
    input("\nPress ENTER to return to menu...")

# ======================
# PASSWORD CHECKER
# ======================
def password_strength():
    clear()
    print(f"{CYAN}=== PASSWORD CHECKER ==={RESET}\n")
    pwd = input("Enter password: ")
    score = 0
    if len(pwd) >= 8: score += 1
    if any(c.isupper() for c in pwd): score += 1
    if any(c.isdigit() for c in pwd): score += 1
    if any(c in "!@#$%^&*()-_=+{}" for c in pwd): score += 1
    levels = ["WEAK","OK","GOOD","STRONG","EXTREME"]
    print("\nPassword strength:", levels[score])
    input("\nPress ENTER to return to menu...")

# ======================
# FILE LOCKER
# ======================
def file_locker():
    clear()
    print(f"{CYAN}=== FILE LOCKER ==={RESET}\n")
    path = input("File or folder path: ").strip()
    if not os.path.exists(path):
        print(f"{RED}Path does not exist!{RESET}")
        time.sleep(1)
        return
    password = getpass("Set password: ")
    def encrypt_file(file_path):
        try:
            with open(file_path,"rb") as f: data=f.read()
            encrypted = bytearray(b ^ 123 for b in data)
            with open(file_path,"wb") as f: f.write(encrypted)
            print(f"{GREEN}Locked:{RESET} {file_path}")
        except: print(f"{RED}Skipped:{RESET} {file_path}")
    if os.path.isfile(path):
        encrypt_file(path)
    elif os.path.isdir(path):
        print(f"{BLUE}Locking all files in folder...{RESET}")
        for root, dirs, files in os.walk(path):
            for file in files:
                encrypt_file(os.path.join(root,file))
    print(f"{GREEN}Done!{RESET}")
    input("\nPress ENTER to return to menu...")

# ======================
# PERFORMANCE MONITOR
# ======================
def performance_monitor():
    clear()
    print(f"{CYAN}=== PERFORMANCE MONITOR ==={RESET}\n")
    print("CTRL+C to stop\n")
    try:
        while True:
            clear()
            print("CPU:", psutil.cpu_percent(), "%")
            print("RAM:", psutil.virtual_memory().percent, "%")
            print("Disk:", psutil.disk_usage('/').percent, "%")
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    input("\nPress ENTER to return to menu...")

# ======================
# CHEAPEST GAME FINDER
# ======================
def cheapest_game_finder():
    clear()
    print(f"{CYAN}=== CHEAPEST GAME FINDER ==={RESET}\n")

    search_type = ""
    while search_type not in ["key", "account"]:
        print("Do you want to search for a game KEY or ACCOUNT?")
        choice = input("Type 'key' or 'account': ").strip().lower()
        if choice in ["key", "account"]:
            search_type = choice
        else:
            print(f"{RED}Invalid choice!{RESET}\n")

    game = input("Enter game name: ").strip()
    if game == "":
        print(f"{YELLOW}No game entered! Returning...{RESET}")
        time.sleep(1)
        return

    # List of websites to search
    websites = {
        "G2A": f"https://www.g2a.com/search?query={requests.utils.quote(game + ' ' + search_type)}",
        "Eneba": f"https://www.eneba.com/search?q={requests.utils.quote(game + ' ' + search_type)}",
        "Instant Gaming": f"https://www.instant-gaming.com/en/search/?q={requests.utils.quote(game + ' ' + search_type)}",
        "Kinguin": f"https://www.kinguin.net/en/catalogsearch/result/?q={requests.utils.quote(game + ' ' + search_type)}",
        "Green Man Gaming": f"https://www.greenmangaming.com/search/{requests.utils.quote(game + ' ' + search_type)}"
    }

    print(f"\nSearching for '{game}' {search_type.upper()} on multiple marketplaces...\n")
    for i, (name, url) in enumerate(websites.items(), start=1):
        print(f"{i}) {name} → Check here: {url}")
        webbrowser.open(url)

    print(f"\n{GREEN}All marketplaces opened in your browser. Check manually for best price!{RESET}")
    input("\nPress ENTER to return to menu...")

def My_all_projects():
    clear()

print("my all projects u can find at github")
print("github : ")

# ======================
# MAIN MENU
# ======================
def menu():
    while True:
        clear()
        print(f"""
{BLUE}========================================
      P C   T O O L K I T   P R O
                 v1.0
========================================{RESET}

1  → PC Cleaner  
2  → System Info  
3  → Network Tools  
4  → Port Scanner  
5  → Fake Error Message  
6  → Password Strength Checker  
7  → File Locker  
8  → Performance Monitor  
9  → Cheapest Game Finder  
10 → My all projects
0 → Exit
""")
        ch = input("Choose option: ").strip()
        if ch == "1": pc_cleaner()
        elif ch == "2": system_info()
        elif ch == "3": network_tools()
        elif ch == "4": port_scanner()
        elif ch == "5": fake_error()
        elif ch == "6": password_strength()
        elif ch == "7": file_locker()
        elif ch == "8": performance_monitor()
        elif ch == "9": cheapest_game_finder()
        elif ch == "10": My_all_projects()
        elif ch == "0":
            clear()
            print(f"{GREEN}Program exited!{RESET}")
            break
        else:
            print(f"{RED}Invalid choice!{RESET}")
            time.sleep(1)

# ======================
# RUN PROGRAM
# ======================
if __name__ == "__main__":
    show_intro()  # Banner sa zobrazí hneď
    menu()
