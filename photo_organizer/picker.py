"""Folder picker utilities using Tkinter."""
from __future__ import annotations

from tkinter import Tk, filedialog


def pick_folder() -> str:
    """Open a folder selection dialog and return the chosen path."""
    root = Tk()
    root.withdraw()
    folder = filedialog.askdirectory()
    root.destroy()
    if not folder:
        raise FileNotFoundError("No folder selected")
    return folder

__all__ = ["pick_folder"]
