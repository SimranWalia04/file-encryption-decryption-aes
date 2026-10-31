
import tkinter as tk
from tkinter import filedialog, messagebox

from cryptography.exceptions import InvalidTag
from main import encrypt_file, decrypt_file



# ---------- GUI ----------

BG = "#0B1220"
PANEL = "#121D30"
ACCENT = "#38BDF8"
TEXT = "#E5EDF7"
MUTED = "#94A3B8"
GREEN = "#34D399"
RED = "#FB7185"


root = tk.Tk()
root.title("CipherSafe | AES File Security")
root.geometry("680x520")
root.minsize(620, 500)
root.configure(bg=BG)

selected_file = tk.StringVar(value="No file selected")
password_var = tk.StringVar()
status_var = tk.StringVar(value="Ready to secure your files")
show_password = tk.BooleanVar(value=False)


def choose_file():
    file_path = filedialog.askopenfilename(
        title="Choose a file",
        filetypes=[
            ("Encrypted and regular files", "*"),
            ("AES encrypted files", "*.aes"),
            ("All files", "*.*"),
        ],
    )

    if file_path:
        selected_file.set(file_path)
        status_var.set("File selected. Enter your password.")
        status_label.config(fg=MUTED)


def toggle_password():
    password_entry.config(
        show="" if show_password.get() else "*"
    )


def run_operation(operation):
    file_path = selected_file.get()
    password = password_var.get()

    if file_path == "No file selected":
        messagebox.showwarning("File required", "Please select a file first.")
        return

    if not password:
        messagebox.showwarning("Password required", "Please enter a password.")
        password_entry.focus_set()
        return

    try:
        if operation == "encrypt":
            output = encrypt_file(file_path, password)
            message = f"File encrypted successfully!\n\nSaved to:\n{output}"
        else:
            output = decrypt_file(file_path, password)
            message = f"File decrypted successfully!\n\nSaved to:\n{output}"

        status_var.set("✓ Operation completed successfully")
        status_label.config(fg=GREEN)
        messagebox.showinfo("Success", message)

    except InvalidTag:
        status_var.set("✕ Decryption failed")
        status_label.config(fg=RED)
        messagebox.showerror(
            "Decryption failed",
            "Incorrect password or the encrypted file has been modified."
        )

    except (FileNotFoundError, FileExistsError, ValueError, OSError) as error:
        status_var.set("✕ Operation could not be completed")
        status_label.config(fg=RED)
        messagebox.showerror("Operation failed", str(error))

    except Exception as error:
        status_var.set("✕ Unexpected error")
        status_label.config(fg=RED)
        messagebox.showerror(
            "Unexpected error",
            f"An unexpected error occurred:\n{error}"
        )

    finally:
        password_var.set()


# Header
header = tk.Frame(root, bg=BG)
header.pack(fill="x", padx=32, pady=(26, 16))

tk.Label(
    header,
    text="◈  CIPHERSAFE",
    font=("Segoe UI", 22, "bold"),
    fg=ACCENT,
    bg=BG,
).pack(anchor="w")

tk.Label(
    header,
    text="AES-256-GCM  •  FILE ENCRYPTION & DECRYPTION",
    font=("Segoe UI", 9, "bold"),
    fg=MUTED,
    bg=BG,
).pack(anchor="w", pady=(5, 0))


# Main panel
panel = tk.Frame(root, bg=PANEL, highlightthickness=1,
                 highlightbackground="#26364F")
panel.pack(fill="both", expand=True, padx=32, pady=(0, 18))

tk.Label(
    panel,
    text="Secure your files",
    font=("Segoe UI", 16, "bold"),
    fg=TEXT,
    bg=PANEL,
).pack(anchor="w", padx=22, pady=(20, 4))

tk.Label(
    panel,
    text="Choose a file and enter a password to continue.",
    font=("Segoe UI", 10),
    fg=MUTED,
    bg=PANEL,
).pack(anchor="w", padx=22, pady=(0, 16))


# File selection
file_frame = tk.Frame(panel, bg="#0B1424",
                      highlightthickness=1,
                      highlightbackground="#30435E")
file_frame.pack(fill="x", padx=22, pady=(0, 18))

file_text = tk.Label(
    file_frame,
    textvariable=selected_file,
    font=("Segoe UI", 9),
    fg=TEXT,
    bg="#0B1424",
    wraplength=390,
    justify="left",
    anchor="w",
)
file_text.pack(side="left", fill="x", expand=True, padx=12, pady=14)

tk.Button(
    file_frame,
    text="Browse",
    command=choose_file,
    font=("Segoe UI", 9, "bold"),
    fg=BG,
    bg=ACCENT,
    activebackground="#7DD3FC",
    relief="flat",
    cursor="hand2",
    padx=14,
    pady=7,
).pack(side="right", padx=10, pady=10)


# Password
tk.Label(
    panel,
    text="PASSWORD",
    font=("Segoe UI", 9, "bold"),
    fg=MUTED,
    bg=PANEL,
).pack(anchor="w", padx=22, pady=(0, 7))

password_entry = tk.Entry(
    panel,
    textvariable=password_var,
    show="*",
    font=("Segoe UI", 11),
    bg="#0B1424",
    fg=TEXT,
    insertbackground=TEXT,
    relief="flat",
    highlightthickness=1,
    highlightbackground="#30435E",
    highlightcolor=ACCENT,
)
password_entry.pack(fill="x", padx=22, ipady=10)

tk.Checkbutton(
    panel,
    text="Show password",
    variable=show_password,
    command=toggle_password,
    font=("Segoe UI", 9),
    fg=MUTED,
    bg=PANEL,
    activebackground=PANEL,
    activeforeground=TEXT,
    selectcolor="#0B1424",
).pack(anchor="w", padx=19, pady=(6, 16))


# Action buttons
button_frame = tk.Frame(panel, bg=PANEL)
button_frame.pack(fill="x", padx=22)

tk.Button(
    button_frame,
    text="🔒  Encrypt File",
    command=lambda: run_operation("encrypt"),
    font=("Segoe UI", 10, "bold"),
    fg=BG,
    bg=ACCENT,
    activebackground="#7DD3FC",
    relief="flat",
    cursor="hand2",
    pady=11,
).pack(side="left", fill="x", expand=True, padx=(0, 6))

tk.Button(
    button_frame,
    text="🔓  Decrypt File",
    command=lambda: run_operation("decrypt"),
    font=("Segoe UI", 10, "bold"),
    fg=TEXT,
    bg="#26364F",
    activebackground="#354A68",
    activeforeground=TEXT,
    relief="flat",
    cursor="hand2",
    pady=11,
).pack(side="left", fill="x", expand=True, padx=(6, 0))


# Status and footer
status_label = tk.Label(
    root,
    textvariable=status_var,
    font=("Segoe UI", 9),
    fg=MUTED,
    bg=BG,
)
status_label.pack(pady=(0, 5))

tk.Label(
    root,
    text="LOCAL FILE PROCESSING  •  AES-GCM AUTHENTICATED ENCRYPTION",
    font=("Segoe UI", 8),
    fg="#64748B",
    bg=BG,
).pack(pady=(0, 14))


root.mainloop()
