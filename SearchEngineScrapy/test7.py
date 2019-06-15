# Python program to print nodes at distance k from a given node

# A binary tree node
class Node:
    # A constructor to create a new node
    def __init__(self, data):
        self.val = data
        self.left = None
        self.right = None


def morris(root):
    current = root
    res=[]
    while current!=None:
        if current.left!=None:
            temp = current.left
            while temp.right!=  None and temp.right!=current:
                temp = temp.right
            if temp.right==None:
                temp.right = current
                current = current.left
            else:
                temp.right= None
                print(current.val)
                current=current.right

        else:
            print(current.val)
            current=current.right






# Driver program to test above function
#    1
#   / \

#  2     3
# /  \  /
#4  5  6


root = Node(1)
root.left = Node(2)
root.right   = Node(3);
root.left.left   = Node(4);
root.left.right  = Node(5);
root.right.left = Node(6);
# root.right.right.left   = Node(3);
# root.right.right.right  = Node(4);
print(morris(root))