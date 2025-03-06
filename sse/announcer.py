import queue
from tools.logger import logger


# Support 10k users~
class MessageAnnouncer:
    def __init__(self):
        self.listeners = {}

    def listen(self, client_addr):
        client_id = client_addr  # Get client IP address as the unique identifier
        if client_id not in self.listeners:
            self.listeners[client_id] = []  # Initialize an empty list
        q = queue.Queue(maxsize=5)
        self.listeners[client_id].append(q)
        return q

    def announce(self, msg, client_addr):
        client_id = client_addr
        if client_id in self.listeners:
            messages = self.listeners[client_id]
            # print(self.listeners)
            # print(messages)
            for i in reversed(range(len(messages))):
                try:
                    messages[i].put_nowait(msg)
                except queue.Full:
                    del messages[i]
