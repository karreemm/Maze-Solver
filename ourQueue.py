class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class OurQueue:
    def __init__(self):
        self.head = None  
        self.tail = None  
        self.length = 0   

    def add(self, item):
        new_node = Node(item)
        if self.is_empty():
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self.length += 1 

    def pop(self):
        if self.is_empty():
            return "Queue is empty"
        popped_value = self.head.value
        self.head = self.head.next
        if self.head is None: 
            self.tail = None
        self.length -= 1
        return popped_value

    def is_empty(self):
        return self.head is None

    def size(self):
        return self.length
