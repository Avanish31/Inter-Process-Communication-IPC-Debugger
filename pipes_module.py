from collections import deque

class Pipe:
    def __init__(self, capacity=5):
        self.buffer = deque()
        self.capacity = capacity

    def write(self, process, data):
        if len(self.buffer) >= self.capacity:
            process.waiting = True
            return False
        self.buffer.append(data)
        process.waiting = False
        return True

    def read(self, process):
        if len(self.buffer) == 0:
            process.waiting = True
            return None
        process.waiting = False
        return self.buffer.popleft()