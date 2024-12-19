class OurQueue:
    def __init__(self):
        self.queue = []

    def add(self, item):
        self.queue.append(item)

    def pop(self):
        if not self.is_empty():
            return self.queue.pop(0)
        return "Queue is empty"

    def is_empty(self):
        return len(self.queue) == 0

    def size(self):
        return len(self.queue)

    def clear(self):
        self.queue = []
        return "Queue cleared"

    def print_queue(self):
        if not self.is_empty():
            print("Queue:", self.queue)
        else:
            print("Queue is empty")
