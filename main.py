import sys
import time
import threading
import random

from simulation_engine import SimulationEngine, SimulatedProcess
from pipes_module import Pipe
from queue_module import MessageQueue
from shared_memory import SharedMemory
from debugger import Debugger

IPC_TYPE = "pipe"
if len(sys.argv) > 1:
    IPC_TYPE = sys.argv[1]

engine = SimulationEngine()

pipe = Pipe()
mq = MessageQueue()
shared = SharedMemory()

start_time = time.time()

# ---------------- PIPE ----------------
def pipe_writer(p):
    pipe.write(p, random.randint(1, 100))
    print(f"Writer {p.pid} running")

def pipe_reader(p):
    elapsed = time.time() - start_time

    if elapsed < 10:
        data = pipe.read(p)
        if data:
            print(f"Reader {p.pid} read {data}")
    else:
        p.waiting = True
        print("Reader stopped → deadlock")
        time.sleep(1)

# ---------------- QUEUE ----------------
def producer(p):
    mq.produce(p, random.randint(1, 100))
    print(f"Producer {p.pid} running")

def consumer(p):
    elapsed = time.time() - start_time

    if elapsed < 10:
        time.sleep(0.3)
    else:
        time.sleep(2)

    mq.consume(p)
    print(f"Consumer {p.pid} running")

# ---------------- SHARED ----------------
def shared_writer(p):
    elapsed = time.time() - start_time

    if elapsed < 10:
        shared.safe_write(p)
    else:
        shared.unsafe_write(p)

    print(f"Process {p.pid} writing")

# ---------------- SETUP ----------------
if IPC_TYPE == "pipe":
    engine.add_process(SimulatedProcess(1, "writer", pipe_writer))
    engine.add_process(SimulatedProcess(2, "reader", pipe_reader))

elif IPC_TYPE == "queue":
    engine.add_process(SimulatedProcess(1, "producer", producer))
    engine.add_process(SimulatedProcess(2, "producer", producer))
    engine.add_process(SimulatedProcess(3, "consumer", consumer))

elif IPC_TYPE == "shared":
    for i in range(4):
        engine.add_process(SimulatedProcess(i, "writer", shared_writer))

# ---------------- DEBUGGER ----------------
debugger = Debugger(engine, pipe=pipe, queue=mq, shared=shared)
t = threading.Thread(target=debugger.monitor)
t.start()

engine.start()

# ensure max runtime 15 sec
while engine.running:
    if time.time() - start_time > 15:
        print("⏹️ Time limit reached")
        engine.stop()
        break
    time.sleep(1)