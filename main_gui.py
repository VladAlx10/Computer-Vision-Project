import os
import platform
import subprocess
import sys
import tkinter as tk

#Main
def get_python_executable():
    """Get the correct Python executable path based on the current environment."""
    # If running in a virtual environment, use the virtual env's python
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        if platform.system() == "Windows":
            return os.path.join(sys.prefix, 'Scripts', 'python.exe')
        else:
            return os.path.join(sys.prefix, 'bin', 'python')
    # Otherwise use the current python
    return sys.executable


def open_project(script_name):
    """Open a Python script with proper error handling and path resolution."""
    try:
        # Get the directory where this script is located
        current_dir = os.path.dirname(os.path.abspath(__file__))
        script_path = os.path.join(current_dir, script_name)

        # Check if the script exists
        if not os.path.exists(script_path):
            raise FileNotFoundError(f"Script not found: {script_path}")

        # Get the correct Python executable
        python_exe = get_python_executable()

        # Print debug info
        print(f"Launching: {python_exe} {script_path}")

        # Use full paths for reliability
        process = subprocess.Popen([python_exe, script_path],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   text=True)

        # Optional: Check for immediate errors
        returncode = process.poll()
        if returncode is not None and returncode != 0:
            stderr = process.stderr.read()
            raise RuntimeError(f"Failed to start process. Error: {stderr}")

        return True
    except Exception as e:
        show_error(f"Error launching {script_name}: {str(e)}")
        return False


def open_project1():
    """Open the color detection project."""
    open_project("color_detection.py")


def open_project2():
    """Open the sketch filter project."""
    open_project("sketch_filter.py")


def show_error(message):
    """Display an error message in a popup window."""
    error_window = tk.Toplevel(root)
    error_window.title("Error")
    error_window.geometry("400x150")

    tk.Label(error_window, text=message, wraplength=380, fg="red").pack(pady=20)
    tk.Button(error_window, text="OK", command=error_window.destroy).pack()


# Main GUI setup
root = tk.Tk()
root.title("Computer Vision Projects")
root.geometry("400x300")
root.configure(bg="#f0f0f0")

# Title frame
title_frame = tk.Frame(root, bg="#f0f0f0")
title_frame.pack(pady=20)

title_label = tk.Label(title_frame,
                       text="Computer Vision Projects",
                       font=("Arial", 16, "bold"),
                       bg="#f0f0f0")
title_label.pack()

subtitle_label = tk.Label(title_frame,
                          text="Alege un proiect:",
                          font=("Arial", 12),
                          bg="#f0f0f0")
subtitle_label.pack(pady=10)

# Buttons frame
button_frame = tk.Frame(root, bg="#f0f0f0")
button_frame.pack(fill="x", padx=50)

# Project buttons with improved styling
btn1 = tk.Button(button_frame,
                 text="Proiect 1: Color Detection",
                 command=open_project1,
                 width=30,
                 height=2,
                 bg="#4CAF50",
                 fg="white",
                 font=("Arial", 10, "bold"),
                 relief=tk.RAISED,
                 cursor="hand2")
btn1.pack(pady=10, fill="x")

btn2 = tk.Button(button_frame,
                 text="Proiect 2: Sketch Filter App",
                 command=open_project2,
                 width=30,
                 height=2,
                 bg="#2196F3",
                 fg="white",
                 font=("Arial", 10, "bold"),
                 relief=tk.RAISED,
                 cursor="hand2")
btn2.pack(pady=10, fill="x")

# Status indicator
status_frame = tk.Frame(root, bg="#f0f0f0")
status_frame.pack(side=tk.BOTTOM, fill="x", pady=10)

status_label = tk.Label(status_frame,
                        text="Ready",
                        font=("Arial", 8),
                        fg="#555555",
                        bg="#f0f0f0")
status_label.pack(side=tk.RIGHT, padx=10)


# Check if files exist on startup
def check_files():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    missing_files = []

    for script in ["color_detection.py", "sketch_filter.py"]:
        if not os.path.exists(os.path.join(current_dir, script)):
            missing_files.append(script)

    if missing_files:
        show_error(
            f"Warning: The following files are missing:\n{', '.join(missing_files)}\n\nPlease make sure these files are in the same directory as this script.")


# Call the file check after a short delay
root.after(500, check_files)

# Start the GUI
if __name__ == "__main__":
    root.mainloop()