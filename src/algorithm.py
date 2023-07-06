from abc import ABC, abstractmethod
import threading

import graph
from debug import debug


class Algorithm(ABC):
    name = ""
    description = ""
    barrier = threading.Barrier(2)
    finished = False
    window = None

    def __init__(self, name, description, window):
        self.name = name
        self.description = description
        self.window = window

    # call this method to start the algorithm
    def start(self, graph):
        debug("Starting algorithm: " + self.name)
        self.finished = False
        self.barrier.reset() # reset barrier
        thread = threading.Thread(target=self.run, args=(graph,)) # create thread to execute algorithm
        thread.start() # start thread

    # the algorithm should be implemented in this method, and should wait with self.pause() before each step
    @abstractmethod
    def run(self, graph):
        pass

    # call this method to execute the next step in the algorithm, releasing the barrier
    def step(self):
        if not self.finished:
            debug("Executing next step in algorithm: " + self.name)
            self.barrier.wait()

    def pause(self):
        self.window.update_graph() # this is executed in this thread, maybe pass message to main thread?
        self.barrier.wait()

    def kill(self):
        debug("Killing algorithm: " + self.name)
        self.barrier.abort()


class TestAlgorithm(Algorithm):
    def __init__(self, window):
        super().__init__("Test Algorithm", "This is a test algorithm that colors all nodes", window)

    def run(self, graph):
        self.pause()
        for node in graph.nodes:
            node.color = "red"
            self.pause()
        self.finished = True
        debug("Algorithm finished: " + self.name)