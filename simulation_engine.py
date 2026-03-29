import time
import threading

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


class SimulationEngine:
    def __init__(self):
        self.processes = []
        self.threads = []
        self.running = True

    def add_process(self, process):
        self.processes.append(process)

    def start(self):
        for p in self.processes:
            t = threading.Thread(target=p.run, args=(self,))
            t.start()
            self.threads.append(t)

    def stop(self):
        self.running = False
        for t in self.threads:
            t.join()