import threading

class SharedMemory:
    def __init__(self):
        self.value = 0
        self.lock = threading.Lock()
        self.write_count = 0

    def safe_write(self, process):
        with self.lock:
            self.value += 1
        process.waiting = False

    def unsafe_write(self, process):
        temp = self.value
        temp += 1
        self.value = temp
        self.write_count += 1
        process.waiting = False

    def reset(self):
        self.write_count = 0