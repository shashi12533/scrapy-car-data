# A complete working Python program to find length of a
# Linked List iteratively

# Node class
class newNode:
    # Function to initialise the node object
    def __init__(self, data):
        self.data = data  # Assign data
        self.next = None  # Initialize next as null
        self.down = None


# Linked List class contains a Node object
class LinkedList:

    # Function to initialize head
    def __init__(self,root):
        self.head = root

    # This function is in LinkedList class. It inserts
    # a new node at the beginning of Linked List.
    # iteratively, given 'node' as starting node.
    def getCount(self,head):
       next  = head.next
       if head.down:
           head.next = self.getCount(head.down)
       if next:
           head.next = self.getCount((next))



if __name__ == '__main__':
    head = newNode(1)
    head.next = newNode(2)
    head.next.next = newNode(3)
    head.next.next.next = newNode(4)
    head.next.down = newNode(7)
    # head.next.down.down = newNode(9)
    # head.next.down.down.down = newNode(14)
    # head.next.down.down.down.down= newNode(15)
    # head.next.down.down.down.down.next= newNode(23)
    # head.next.down.down.down.down.next.down= newNode(24)
    # head.next.down.next = newNode(8)
    # head.next.down.next.down = newNode(16)
    # head.next.down.next.down.down = newNode(17)
    # head.next.down.next.down.down.next= newNode(18)
    # head.next.down.next.down.down.next.next= newNode(19)
    # head.next.down.next.down.down.next.next.next= newNode(20)
    # head.next.down.next.down.down.next.next.next.down= newNode(21)
    # head.next.down.next.next = newNode(10)
    # head.next.down.next.next.down = newNode(11)
    # head.next.down.next.next.next = newNode(12)
    llist = LinkedList(head)

print("Count of nodes is :", llist.getCount(head))
