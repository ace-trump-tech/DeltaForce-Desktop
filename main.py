# main.py
import base64
import sys
import tkinter as tk
from tkinter import messagebox
import yaml

# Import privilege escalation and launcher from data.bin subpackage
from data.bin.launcher import run_as_admin, run_installer
# Import hidden message functions from data.crypto
from data.crypto import get_ok_message, get_warn_message


def _decode_b64_msg(func):
    """Decode a base64-encoded message retrieved from the binary file."""
    return base64.b64decode(func()).decode("utf-8")

def main():
    # Request administrator privileges (UAC prompt if not already admin)
    run_as_admin()

    # Load configuration from YAML file
    with open("config.yaml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    # Create hidden root window for dialogs
    root = tk.Tk()
    root.withdraw()

    # Show the initial warning dialog
    result = messagebox.askyesno(
        title=config['warning_message']['title'],
        message=config['warning_message']['text'],
        icon='warning'
    )

    if result:
        # Run the local installer (Lockhead.exe)
        success = run_installer()
        if success:
            # Show the success message retrieved from binary file
            messagebox.showinfo("Notice", _decode_b64_msg(get_ok_message))
        else:
            messagebox.showerror("Error", "Failed to start installer. Please run Lockhead.exe manually.")
    else:
        # User insists on using cheats – show warning
        messagebox.showwarning("Risk Warning", _decode_b64_msg(get_warn_message))

    root.destroy()
    sys.exit(0)

if __name__ == "__main__":
    main()
