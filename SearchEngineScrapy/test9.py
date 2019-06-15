# Python3 program to remove duplicate
# nodes from a sorted linked list

# Node class
class Node:

    # Constructor to initialize
    # the node object
    def __init__(self, data):
        self.val = data
        self.next = None


class LinkedList:

    # Function to initialize head
    def __init__(self):
        self.head = None

    # Function to insert a new node
    # at the beginning
    def push(self, new_data):
        new_node = Node(new_data)
        new_node.next = self.head
        self.head = new_node


    def printList(self,m):
        temp = self.head
        while (temp):
            print(temp.val, end=' ')
            temp = temp.next

    # This function removes duplicates
    # from a sorted list
    def removeDuplicates(self):
        def wrapper(head1,head2):
            if head1==None:
                return
            wrapper(head1.next,head2)
            temp = not head2.next
            head2.next = head1
            head1.next = temp




        wrapper(self.head,self.head)

    # Driver Code


llist = LinkedList()

llist.push(20)
llist.push(13)
llist.push(14)
llist.push(12)
llist.push(10)
llist.push(9)
# print("Created Linked List: ")
# llist.printList()
# print()
print("Linked List after removing",
      "duplicate elements:")
m = llist.removeDuplicates()
print(m)
llist.printList(m)

# This code is contributed by
# Dushyant Pathak.
