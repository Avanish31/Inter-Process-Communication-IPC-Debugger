import time
import threading
# ─────────────────────────────────────────
# PIPE IMPLEMENTATION
# ─────────────────────────────────────────
class Pipe:
    def __init__(self):
        self.data = None
        self.lock = threading.Lock()
        self.message_count = 0

    def write(self, msg):
        with self.lock:
            self.data = msg
            self.message_count += 1

    def read(self):
        with self.lock:
            return self.data
# ─────────────────────────────────────────
# MESSAGE QUEUE IMPLEMENTATION
# ─────────────────────────────────────────
class MessageQueue:
    def __init__(self):
        self.q = []
        self.lock = threading.Lock()

    def send(self, msg):
        with self.lock:
            self.q.append(msg)

    def receive(self):
        with self.lock:
            if self.q:
                return self.q.pop(0)
            return None

    def get_all(self):
        with self.lock:
            return list(self.q)

    def size(self):
        with self.lock:
            return len(self.q)


# ─────────────────────────────────────────
# SHARED MEMORY IMPLEMENTATION
# ─────────────────────────────────────────
class SharedMemory:
    def __init__(self):
        self.value = None
        self.lock = threading.Lock()
        self.write_count = 0

    def write(self, val):
        with self.lock:
            self.value = val
            self.write_count += 1

    def read(self):
        with self.lock:
            return self.value


# ─────────────────────────────────────────
# SIMULATED PROCESS
# ─────────────────────────────────────────
class SimulatedProcess:
    def __init__(self, pid, role, action):
        self.pid = pid
        self.role = role
        self.action = action
        self.waiting = False

    def run(self, engine):
        while engine.running:
            self.action(self)
            time.sleep(0.2)


# ─────────────────────────────────────────
# MAIN SIMULATION ENGINE
# ─────────────────────────────────────────
class SimulationEngine:
    def __init__(self):
        self.processes = []
        self.threads = []
        self.running = True

        # ✅ IPC Components (REQUIRED FOR GUI)
        self.pipe = Pipe()
        self.queue = MessageQueue()
        self.shared = SharedMemory()

    def add_process(self, process):
        self.processes.append(process)

    def start(self):
        self.running = True
        for p in self.processes:
            t = threading.Thread(target=p.run, args=(self,))
            t.daemon = True
            t.start()
            self.threads.append(t)

    def stop(self):
        self.running = False
        for t in self.threads:
            t.join()