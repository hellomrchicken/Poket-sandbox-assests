import tkinter as tk
from tkinter import messagebox, simpledialog
import subprocess
import os
import sys
import time

# ============================================================
# POCKET SANDBOX LAUNCHER
# ============================================================

GAME_FOLDER = r"C:\Users\Edens\Downloads\sandbox game assests"
CLIENT_FILE = "client.py"
SERVER_FILE = "server.py"
SINGLEPLAYER_FILE = "sandbox_game.py"

# ============================================================
# PROCESS HELPERS
# ============================================================

def launch_python(filename, args=None):
    """Launch a Python file from the sandbox folder."""
    path = os.path.join(GAME_FOLDER, filename)

    if not os.path.isfile(path):
        messagebox.showinfo(
            "Not Available",
            f"{filename} is not available at this time."
        )
        return None

    try:
        command = [sys.executable, path]
        if args:
            command.extend(args)

        return subprocess.Popen(
            command,
            cwd=GAME_FOLDER
        )
    except Exception as e:
        messagebox.showerror(
            "Launch Error",
            f"Could not start {filename}.\n\n{e}"
        )
        return None


def available(filename):
    return os.path.isfile(os.path.join(GAME_FOLDER, filename))


# ============================================================
# SINGLEPLAYER
# ============================================================

def launch_singleplayer():
    launch_python(SINGLEPLAYER_FILE)


# ============================================================
# MULTIPLAYER
# ============================================================

def join_multiplayer():
    if not available(CLIENT_FILE):
        messagebox.showinfo(
            "Not Available",
            "client.py is not available at this time."
        )
        return

    ip = simpledialog.askstring(
        "Join Multiplayer",
        "Enter the server IP address:\n\n"
        "Use 127.0.0.1 if the server is on this PC.",
        initialvalue="127.0.0.1",
        parent=root
    )

    if ip is None:
        return

    ip = ip.strip()

    if not ip:
        messagebox.showerror(
            "Invalid IP",
            "Please enter a server IP address."
        )
        return

    launch_python(CLIENT_FILE, ["--ip", ip])


# ============================================================
# HOST SERVER
# ============================================================

def host_server():
    if not available(SERVER_FILE):
        messagebox.showinfo(
            "Not Available",
            "server.py is not available at this time."
        )
        return None

    return launch_python(SERVER_FILE)


# ============================================================
# HOST & PLAY
# ============================================================

def host_and_play():
    """Start the server, wait briefly, then launch the local client."""
    if not available(SERVER_FILE):
        messagebox.showinfo(
            "Not Available",
            "server.py is not available at this time."
        )
        return

    if not available(CLIENT_FILE):
        messagebox.showinfo(
            "Not Available",
            "client.py is not available at this time."
        )
        return

    server_process = host_server()

    if server_process is None:
        return

    # Give the TCP server a moment to bind to port 25565.
    root.after(
        800,
        lambda: launch_python(CLIENT_FILE, ["--ip", "127.0.0.1"])
    )


# ============================================================
# BUTTON HELPERS
# ============================================================

def make_button(parent, text, command, required_files=None):
    if required_files is None:
        required_files = []

    exists = all(available(filename) for filename in required_files)

    if exists:
        bg = "#5865f2"
        hover = "#4752c4"
        fg = "white"
    else:
        bg = "#3a3c43"
        hover = "#3a3c43"
        fg = "#777b84"

    def click():
        if not exists:
            missing = [
                filename
                for filename in required_files
                if not available(filename)
            ]
            messagebox.showinfo(
                "Not Available",
                "This is not available at this time.\n\n"
                + "Missing: " + ", ".join(missing)
            )
            return

        command()

    button = tk.Button(
        parent,
        text=text,
        command=click,
        font=("Arial", 13, "bold"),
        bg=bg,
        fg=fg,
        activebackground=hover,
        activeforeground="white",
        relief="flat",
        bd=0,
        width=30,
        height=2,
        cursor="hand2"
    )
    button.pack(pady=6)
    return button


# ============================================================
# WINDOW
# ============================================================

root = tk.Tk()
root.title("Pocket Sandbox")
root.geometry("560x760")
root.resizable(False, False)
root.configure(bg="#1e1f22")


# ============================================================
# HEADER
# ============================================================

title = tk.Label(
    root,
    text="POCKET SANDBOX",
    font=("Arial", 30, "bold"),
    fg="white",
    bg="#1e1f22"
)
title.pack(pady=(30, 0))

subtitle = tk.Label(
    root,
    text="3D Physics Sandbox",
    font=("Arial", 12),
    fg="#949ba4",
    bg="#1e1f22"
)
subtitle.pack(pady=(5, 20))


# ============================================================
# GAME BUTTONS
# ============================================================

make_button(
    root,
    "▶  SINGLEPLAYER",
    launch_singleplayer,
    [SINGLEPLAYER_FILE]
)

make_button(
    root,
    "🌐  JOIN MULTIPLAYER",
    join_multiplayer,
    [CLIENT_FILE]
)

make_button(
    root,
    "🖥  HOST SERVER",
    host_server,
    [SERVER_FILE]
)

make_button(
    root,
    "🚀  HOST & PLAY",
    host_and_play,
    [SERVER_FILE, CLIENT_FILE]
)


# ============================================================
# MULTIPLAYER INFO
# ============================================================

info_frame = tk.Frame(
    root,
    bg="#2b2d31"
)
info_frame.pack(
    fill="x",
    padx=55,
    pady=(15, 12)
)

info_title = tk.Label(
    info_frame,
    text="MULTIPLAYER",
    font=("Arial", 11, "bold"),
    fg="white",
    bg="#2b2d31"
)
info_title.pack(pady=(10, 4))

info_text = tk.Label(
    info_frame,
    text=(
        "HOST & PLAY starts the server and your game.\n"
        "Friends join using your PC's IPv4 address.\n"
        "Server port: 25565"
    ),
    font=("Arial", 9),
    fg="#b5bac1",
    bg="#2b2d31",
    justify="center"
)
info_text.pack(pady=(0, 10))


# ============================================================
# FILE STATUS
# ============================================================

status_frame = tk.Frame(
    root,
    bg="#2b2d31"
)
status_frame.pack(
    fill="x",
    padx=55,
    pady=5
)

status_title = tk.Label(
    status_frame,
    text="GAME FILES",
    font=("Arial", 11, "bold"),
    fg="white",
    bg="#2b2d31"
)
status_title.pack(pady=(10, 8))

if os.path.isdir(GAME_FOLDER):
    files = [
        f for f in os.listdir(GAME_FOLDER)
        if f.lower().endswith(".py")
    ]

    if files:
        for filename in sorted(files):
            label = tk.Label(
                status_frame,
                text="✓  " + filename,
                font=("Arial", 9),
                fg="#57f287",
                bg="#2b2d31"
            )
            label.pack(anchor="w", padx=20)
    else:
        label = tk.Label(
            status_frame,
            text="No Python game files found.",
            font=("Arial", 9),
            fg="#ed4245",
            bg="#2b2d31"
        )
        label.pack(pady=10)
else:
    label = tk.Label(
        status_frame,
        text="Game folder not found.",
        font=("Arial", 9),
        fg="#ed4245",
        bg="#2b2d31"
    )
    label.pack(pady=10)


# ============================================================
# FOLDER BUTTON
# ============================================================

def open_folder():
    if os.path.isdir(GAME_FOLDER):
        os.startfile(GAME_FOLDER)
    else:
        messagebox.showinfo(
            "Folder Missing",
            "The Pocket Sandbox game folder could not be found."
        )


folder_button = tk.Button(
    root,
    text="📁  OPEN GAME FOLDER",
    command=open_folder,
    font=("Arial", 10, "bold"),
    fg="#b5bac1",
    bg="#1e1f22",
    activebackground="#1e1f22",
    activeforeground="white",
    relief="flat",
    bd=0,
    cursor="hand2"
)
folder_button.pack(pady=5)


# ============================================================
# QUIT
# ============================================================

quit_button = tk.Button(
    root,
    text="QUIT",
    command=root.destroy,
    font=("Arial", 10, "bold"),
    fg="#b5bac1",
    bg="#1e1f22",
    activebackground="#1e1f22",
    activeforeground="white",
    relief="flat",
    bd=0,
    cursor="hand2"
)
quit_button.pack(pady=5)


# ============================================================
# START
# ============================================================

root.mainloop()
