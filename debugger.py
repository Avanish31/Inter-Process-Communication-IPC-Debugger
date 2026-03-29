import time

class Debugger:
    def __init__(self, engine, pipe=None, queue=None, shared=None):
        self.engine = engine
        self.pipe = pipe
        self.queue = queue
        self.shared = shared

    def check_deadlock(self):
        waiting = [p for p in self.engine.processes if p.waiting]
        if len(waiting) == len(self.engine.processes) and len(waiting) > 0:
            print("🔴 Deadlock detected! Stopping...")
            self.engine.stop()

    def check_bottleneck(self):
        if self.queue:
            if self.queue.qsize() >= 5:
                print("🟡 Bottleneck detected! Stopping...")
                self.engine.stop()

    def check_race(self):
        if self.shared:
            if self.shared.write_count > 5:
                print("🟠 Race condition detected! Stopping...")
                self.engine.stop()
            self.shared.reset()

    def monitor(self):
        while self.engine.running:
            self.check_deadlock()
            self.check_bottleneck()
            self.check_race()
            time.sleep(1)