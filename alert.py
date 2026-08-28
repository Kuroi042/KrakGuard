import tkinter as tk
from tkinter import messagebox

# Hide the main Tkinter root window
root = tk.Tk()
root.withdraw()

# Show alert popup
messagebox.showwarning("Alert", "ALERT: Action Detected!")
root.destroy()