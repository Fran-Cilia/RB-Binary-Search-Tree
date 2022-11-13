class Node(object):
    def __init__(self, data):
        self.parent = None
        self.left = None
        self.right = None
        self.data = data
        self.color = 1  # 1 represents red


class Tree(object):
    # Binary Search Tree
    # class constants
    PREORDER = 1
    INORDER = 2
    POSTORDER = 3

    def __init__(self):
        # Do not create any other private variables.
        # You may create more helper methods as needed.
        self.root = None

    def print(self):
        # Print the data of all nodes in order
        self.__print(self.root)

    def __print(self, curr_node):
        # Recursively print a subtree (in order), rooted at curr_node
        if curr_node is not None:
            self.__print(curr_node.left)
            print(str(curr_node.data), end=' ')  # save space
            self.__print(curr_node.right)      

    def __get_sibling(self, node):
        # Helper function that gets sibling of a node
        if node.parent:
            temp = node.parent
            if temp.left != node:
                return temp.left
            elif temp.right != node:
                return temp.right
        return None     

    def __is_left_child(self, node):
        # Helper function that returns true if node is left child
        if node.parent:
            parent = node.parent
            return parent.left == node

    def __rotate_right(self, node):
        # Helper function that does one rotation to the right
        x = node.left
        node.left = x.right

        if x.right:
            x.right.parent = node
        x.parent = node.parent
        if node.parent == None:
            self.root = x    
        elif node == node.parent.right:
            node.parent.right = x
        else:
            node.parent.left = x
        
        x.right = node
        node.parent = x


    def __rotate_left(self, node):
        # Helper function that does on rotation to the left
        x = node.right
        node.right = x.left 

        if x.left:
            x.left.parent = node
        
        x.parent = node.parent
        if node.parent == None:
            self.root = x
        elif node == node.parent.left:
            node.parent.left = x
        else:
            node.parent.right = x

        x.left = node
        node.parent = x            

    def insert(self, data):
        # Find the right spot in the tree for the new node
        # Make sure to check if anything is in the tree
        # Hint: if a node n is None, calling n.data will cause an error

        # Case 1: tree is empty
        if self.root == None:
            self.root = Node(data)
            self.root.color = 0
            return

        # Finds the right spot in the tree for the new node
        temp = self.root
        parent = None
        while temp:
            parent = temp
            if data < temp.data:
                temp = temp.left   
            else:
                temp = temp.right
            
        if data < parent.data:
            parent.left = Node(data)
            new = parent.left
            parent.left.parent = parent
        else:
            parent.right = Node(data)
            new = parent.right
            parent.right.parent = parent

        if new.parent.parent == None:
            return

        self.__fix_insert(new)



    def __fix_insert(self, node):
        
        # helper function to fix any conditions that may have been broken after insertion
        while node.parent.color == 1:
            
            uncle = self.__get_sibling(node.parent)
            # Case 2: uncle is red
            if uncle and uncle.color == 1:
                node.parent.color = 0
                uncle.color = 0
                node.parent.parent.color = 1
                node = node.parent.parent
            # Case 3a: uncle of new node is black and it forms a left side line
            elif self.__is_left_child(node) and self.__is_left_child(node.parent):
                node.parent.color = 0
                node.parent.parent.color = 1
                self.__rotate_right(node.parent.parent)
            # Case 3a: uncle of new node is black and it forms a right side line
            elif self.__is_left_child(node) == False and self.__is_left_child(node.parent) == False:
                node.parent.color = 0
                node.parent.parent.color = 1
                self.__rotate_left(node.parent.parent)
            # Case 3b: uncle of new node is black and it forms a left triangle
            elif self.__is_left_child(node) == False and self.__is_left_child(node.parent):
                node = node.parent
                self.__rotate_left(node)
                node.parent.color = 0
                node.parent.parent.color = 1
                self.__rotate_right(node.parent.parent)
            # Case 3b: uncle of new node is black and it forms a right triangle
            elif self.__is_left_child(node) and self.__is_left_child(node.parent) == False:
                node = node.parent
                self.__rotate_right(node)
                node.parent.color = 0
                node.parent.parent.color = 1
                self.__rotate_left(node.parent.parent)
            

            if node == self.root:
                break

        self.root.color = 0
            

            
            


    # def __fix_insert(self, node):
    #     # helper function to fix any conditions that may have been broken after insertion
    #     while node.parent.color == 1:

    #         if self.__is_left_child(node.parent) == False:  #if parent is right child
    #             uncle = self.__get_sibling(node.parent)
    #             if uncle and uncle.color == 1:
    #                 uncle.color = 0
    #                 node.parent.color = 0
    #                 node.parent.parent.color = 1
    #                 node = node.parent.parent

    #             else:
    #                 if self.__is_left_child(node):
    #                     node = node.parent
    #                     self.__rotate_right(node)
    #                 node.parent.color = 0
    #                 node.parent.parent.color = 1
    #                 self.__rotate_left(node.parent.parent)

    #         else:
    #             uncle = self.__get_sibling(node.parent)
    #             if uncle and uncle.color == 1:
    #                 uncle.color = 0
    #                 node.color = 0
    #                 node.parent.parent.color =  1
    #                 node = node.parent.parent
    #             else:
    #                 if self.__is_left_child(node.parent) == False:
    #                     node = node.parent
    #                     self.__rotate_left(node)
    #                 node.parent.color = 0
    #                 node.parent.parent.color = 1
    #                 self.__rotate_right(node.parent.parent)
            
    #         if node == self.root:
    #             break

    #     self.root.color = 0
                
            


    # def insert(self, data):
    #     # Find the right spot in the tree for the new node
    #     # Make sure to check if anything is in the tree
    #     # Hint: if a node n is None, calling n.data will cause an error
        
    #     # Case 1: tree is empty
    #     if self.root == None:
    #         self.root = Node(data)
    #         self.root.color = 0
    #         return

    #     # Finds the right spot in the tree for the new node
    #     temp = self.root
    #     parent = None
    #     while temp:
    #         parent = temp
    #         if data < temp.data:
    #             temp = temp.left   
    #         else:
    #             temp = temp.right
            
    #     if data < parent.data:
    #         parent.left = Node(data)
    #         new = parent.left
    #         parent.left.parent = parent
    #     else:
    #         parent.right = Node(data)
    #         new = parent.right
    #         parent.right.parent = parent

    #     if parent.color == 1:
    #         # Case 2: uncle of new node is red
    #         uncle = self.__get_sibling(parent)
    #         if uncle and uncle.color == 1:
    #             self.__recolor(new)
                
    #         # Case 3: uncle of new node is black
    #         else:
    #             # Case 3a: uncle of new node is black and it forms a left side line
    #             if self.__is_left_child(new) and self.__is_left_child(parent):
    #                 self.__ll(parent, parent.parent, self.__is_left_child(parent.parent))
    #             # Case 3a: uncle of new node is black and it forms a right side line
    #             elif self.__is_left_child(new) == False and self.__is_left_child(parent) == False:
    #                 self.__rr(parent, parent.parent, self.__is_left_child(parent.parent))

    #             # Case 3b: uncle of new node is black and it forms a left side triangle
    #             elif self.__is_left_child(new) == False and self.__is_left_child(parent):
    #                 grandparent = parent.parent
    #                 grandparent.left = self.__rotate_left(parent)
    #                 self.__rr(grandparent.left, grandparent, self.__is_left_child(grandparent))

    #             # Case 3b: uncle of new node is black and it forms a right side triangle
    #             elif self.__is_left_child(new) and self.__is_left_child(parent) == False:
    #                 grandparent = parent.parent
    #                 grandparent.right = self.__rotate_right(parent)
    #                 self.__ll(grandparent.right, grandparent, self.__is_left_child(grandparent))





# def main():
#     t = Tree()
    # t.insert(1)
    # t.insert(2)
    # t.insert(3)
    # t.insert(4)
    # t.insert(5)
    # print(t.root.data)
    # print(t.root.right.data)
    # print(t.root.right.left.data)
    # print(t.root.right.right.data)
    # print("\n")
    # t.insert(6)
    # print(t.root.data)
    # print(t.root.right.data)
    # print(t.root.right.left.data)
    # print(t.root.right.right.data)
    # print(t.root.right.right.right.data)
    # print("\n")
    # t.insert(7)
    # print(t.root.data)
    # print(t.root.right.data)
    # print(t.root.right.left.data)
    # print(t.root.right.right.data)
    # print(t.root.right.right.right.data)
    # print(t.root.right.right.left.data)
    # print("\n")
    # t.insert(10)
    # t.insert(9)
    # t.insert(8)
    # t.insert(7)
    # t.insert(6)
    # print(t.root.data)
    # print(t.root.left.data)
    # print(t.root.left.left.data)
    # print(t.root.left.right.data)
    # print("\n")
    # t.insert(5)
    # print(t.root.data)
    # print(t.root.left.data)
    # print(t.root.left.left.data)
    # print(t.root.left.right.data)
    # print(t.root.left.left.left.data)
    # print("\n")
    # t.insert(4)
    # print(t.root.color)
    # print(t.root.left.color)
    # print(t.root.left.left.color)
    # print(t.root.left.right.color)
    # print(t.root.left.left.right.color)
    # print(t.root.left.left.left.color)
    # print("\n")
    # t.insert(3)
    # print(t.root.data)
    # print(t.root.left.data)
    # print(t.root.right.data)
    # print(t.root.left.left.data)
    # print(t.root.left.right.data)
    # print(t.root.right.left.data)
    # print(t.root.right.right.data)
    # print(t.root.left.left.left.data)
    # print("\n")
    # t.insert(2)
    # print(t.root.data)
    # print(t.root.left.data)
    # print(t.root.right.data)
    # print(t.root.left.left.data)
    # print(t.root.left.right.data)
    # print(t.root.right.left.data)
    # print(t.root.right.right.data)
    # print(t.root.left.left.left.data)
    # print(t.root.left.left.right.data)
    # t.insert(1)
    # print("\n")
    # print(t.root.data)
    # print(t.root.left.data)
    # print(t.root.right.data)
    # print(t.root.left.left.data)
    # print(t.root.left.right.data)
    # print(t.root.right.left.data)
    # print(t.root.right.right.data)
    # print(t.root.left.left.left.data)
    # print(t.root.left.left.right.data)
    # print(t.root.left.left.left.left.data)
    # t.insert(0)
    # print("\n")
    # print(t.root.data)
    # print(t.root.left.data)
    # print(t.root.right.data)
    # print(t.root.left.left.data)
    # print(t.root.left.right.data)
    # print(t.root.right.left.data)
    # print(t.root.right.right.data)
    # print(t.root.left.left.left.data)
    # print(t.root.left.left.right.data)
    # print(t.root.left.left.left.left.data)
    # print(t.root.left.left.left.right.data)





    
    # t.print()



    
#     t.print()
#     # t.insert(10)
#     # t.insert(11)
#     # t.insert(12)
#     # print(t.root.data)
#     # print(t.root.left.data)
#     # print(t.root.right.data)
#     # print("\n")
#     # t.insert(13)
#     # print(t.root.data)
#     # print(t.root.left.data)
#     # print(t.root.right.data)
#     # print(t.root.right.right.data)
#     # print("\n")
#     # t.insert(14)
#     # print(t.root.data)
#     # print(t.root.left.data)
#     # print(t.root.right.data)
#     # print(t.root.right.right.data)
#     # print(t.root.right.left.data)
#     # t.insert(15)
#     # print("\n")
#     # print(t.root.color)
#     # print(t.root.left.color)
#     # print(t.root.right.color)
#     # print(t.root.right.right.color)
#     # print(t.root.right.left.color)
#     # print(t.root.right.right.right.color)
#     # # print(t.root.left.data)
#     # # print(t.root.left.left.data)
#     # # print(t.root.left.right.data)


    



#main()