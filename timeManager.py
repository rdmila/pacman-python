import time
import heapq


class Event:

    def __init__(self, game):
        self.game = game

    def do(self):
        pass


class TimeEvent(Event):
    def __init__(self, game, delay):
        super().__init__()
        self.delay = delay
        self.time = -1

    def __lt__(self, other):
        return self.time < other.time


class TimeManager:
    def __init__(self):
        self.events = []

    def add_event(self, event):
        current_time = time.process_time()
        event.time = current_time + event.delay
        del event.delay
        heapq.heappush(self.events, event)

    def get_events(self):
        current_time = time.process_time()
        while self.events[0] <= current_time:
            self.events[0].do()
            heapq.heappop(self.events)
