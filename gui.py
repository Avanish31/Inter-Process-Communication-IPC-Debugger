import tkinter as tk
import subprocess

process = None

def run_sim(ipc):
    global process
    stop_sim()
    process = subprocess.Popen(["python", "main.py", ipc])
    status_label.config(text=f"Running: {ipc.upper()}", fg="#00cc66")
    stop_btn.config(state="normal")

def stop_sim():
    global process
    if process:
        process.terminate()
        process = None
    status_label.config(text="Stopped", fg="#cc3333")
    stop_btn.config(state="disabled")

# ── Root Window ──
root = tk.Tk()
root.title("IPC Debugger")
root.geometry("420x520")
root.configure(bg="#1e1e2e")
root.resizable(False, False)

# ── Header ──
header = tk.Frame(root, bg="#12121f", height=70)
header.pack(fill="x")
header.pack_propagate(False)

tk.Label(
    header,
    text="IPC Debugger",
    font=("Segoe UI", 16, "bold"),
    bg="#12121f",
    fg="#ffffff"
).pack(pady=18)

# ── Status ──
status_label = tk.Label(
    root,
    text="● Idle",
    font=("Segoe UI", 10),
    bg="#1e1e2e",
    fg="#555577"
)
status_label.pack(pady=(15, 5))

# ── Divider ──
tk.Frame(root, bg="#2a2a3e", height=1).pack(fill="x", padx=30, pady=5)

# ── Description ──
tk.Label(
    root,
    text="Select an IPC method to simulate:",
    font=("Segoe UI", 10),
    bg="#1e1e2e",
    fg="#888899"
).pack(pady=(10, 20))

# ── Button Style Helper ──
def make_btn(parent, label, sublabel, color, command):
    frame = tk.Frame(parent, bg=color, cursor="hand2")
    frame.pack(fill="x", padx=40, pady=8)

    inner = tk.Frame(frame, bg=color)
    inner.pack(fill="x", padx=15, pady=12)

    tk.Label(
        inner,
        text=label,
        font=("Segoe UI", 11, "bold"),
        bg=color,
        fg="white"
    ).pack(anchor="w")

    tk.Label(
        inner,
        text=sublabel,
        font=("Segoe UI", 8),
        bg=color,
       fg="#ffffff"
    ).pack(anchor="w")

    frame.bind("<Button-1>", lambda e: command())
    inner.bind("<Button-1>", lambda e: command())
    for child in inner.winfo_children():
        child.bind("<Button-1>", lambda e: command())

    return frame

# ── IPC Buttons ──
make_btn(
    root,
    "Pipes",
    "Simulate deadlock using pipes",
    "#1a3a5c",
    lambda: run_sim("pipe")
)

make_btn(
    root,
    "Message Queue",
    "Simulate bottleneck using message queue",
    "#1a3a2a",
    lambda: run_sim("queue")
)

make_btn(
    root,
    "Shared Memory",
    "Simulate race condition using shared memory",
    "#3a2a1a",
    lambda: run_sim("shared")
)

# ── Divider ──
tk.Frame(root, bg="#2a2a3e", height=1).pack(fill="x", padx=30, pady=15)

# ── Stop Button ──
stop_btn = tk.Button(
    root,
    text="⬛  STOP",
    font=("Segoe UI", 11, "bold"),
    bg="#cc3333",
    fg="white",
    activebackground="#aa2222",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    width=20,
    pady=10,
    state="disabled",
    command=stop_sim
)
stop_btn.pack(pady=5)

# ── Footer ──
tk.Label(
    root,
    text="IPC Debugger  •  OS Project",
    font=("Segoe UI", 8),
    bg="#1e1e2e",
    fg="#333344"
).pack(side="bottom", pady=10)

root.mainloop()