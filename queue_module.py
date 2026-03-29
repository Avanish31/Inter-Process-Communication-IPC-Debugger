import queue

class MessageQueue:
    def __init__(self, maxsize=5):
        self.q = queue.Queue(maxsize=maxsize)

    def produce(self, process, data):
        if self.q.full():
            process.waiting = True
            return False
        self.q.put(data)
        process.waiting = False
        return True

    def consume(self, process):
        if self.q.empty():
            process.waiting = True
            return None
        process.waiting = False
        return self.q.get()

    def qsize(self):
        return self.q.qsize()