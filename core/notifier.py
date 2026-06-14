# core/notifier.py
import tkinter as tk
from tkinter import messagebox
import yaml

def show_anti_cheat_warning():
    """Display a standalone warning popup about cheating risks."""
    with open("config.yaml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    root = tk.Tk()
    root.withdraw()
    messagebox.showwarning(
        title=config['warning_message']['title'],
        message=config['warning_message']['text']
    )
    root.destroy()
