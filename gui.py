import tkinter as tk
import subprocess

process = None

def run_sim(ipc):
    global process
    stop_sim()
    process = subprocess.Popen(["python", "main.py", ipc])

def stop_sim():
    global process
    if process:
        process.terminate()
        process = None

root = tk.Tk()
root.title("IPC Debugger")

tk.Label(root, text="Select IPC").pack()

tk.Button(root, text="Pipes (Deadlock)", command=lambda: run_sim("pipe")).pack()
tk.Button(root, text="Queue (Bottleneck)", command=lambda: run_sim("queue")).pack()
tk.Button(root, text="Shared (Race)", command=lambda: run_sim("shared")).pack()

tk.Button(root, text="STOP", command=stop_sim, bg="red").pack()

root.mainloop()