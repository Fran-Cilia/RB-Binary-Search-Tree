class Node(object):
    """
    A class to represent a node in the red black tree
    ...
    Summary
    -------
    Has pointer to the nodes, parent, left, and right nodes. 
    Also has a variable that keeps track of current data and color in the node
    ...
    Attributes
    ----------
    data : int
    """
    def __init__(self, data, left = None, right = None, parent = None, color = 'red'):
        self.data = data
        self.left = left
        self.right = right
        self.parent = parent
        self.color = color

class rb_tree(object):
    PREORDER = 1
    INORDER = 2
    POSTORDER = 3
    # initialize root and size
    def __init__(self):
        self.root = None
        self.sentinel = Node(None, color = 'black')
        self.sentinel.parent = self.sentinel
        self.sentinel.left = self.sentinel
        self.sentinel.right = self.sentinel
    
    def print_tree(self):
        # Print the data of all nodes in order
        self.__print_tree(self.root)
    
    def __print_tree(self, curr_node):
        # Recursively print a subtree (in order), rooted at curr_node
        # Printed in preorder
        if curr_node is not self.sentinel:
            print(str(curr_node.data), end=' ')  # save space
            self.__print_tree(curr_node.left)
            self.__print_tree(curr_node.right)

    def __print_with_colors(self, curr_node):
        # Recursively print a subtree (in order), rooted at curr_node
        # Printed in PREORDER
        # Extracts the color of the node and print it in the format -dataC- where C is B for black and R for red
        if curr_node is not self.sentinel:
            if curr_node.color is "red":
                node_color = "R"
            else:
                node_color = "B"
            print(str(curr_node.data)+node_color, end=' ')  # save space
            self.__print_with_colors(curr_node.left)
            self.__print_with_colors(curr_node.right)

    def print_with_colors(self):
        # Also prints the data of all node but with color indicators
        self.__print_with_colors(self.root)

    def __iter__(self):
        return self.inorder()

    def inorder(self):
        return self.__traverse(self.root, rb_tree.INORDER)

    def preorder(self):
        return self.__traverse(self.root, rb_tree.PREORDER)

    def postorder(self):
        return self.__traverse(self.root, rb_tree.POSTORDER)

    def __traverse(self, curr_node, traversal_type):
        if curr_node is not self.sentinel:
            if traversal_type == self.PREORDER:
                yield curr_node
            yield from self.__traverse(curr_node.left, traversal_type)
            if traversal_type == self.INORDER:
                yield curr_node
            yield from self.__traverse(curr_node.right, traversal_type)
            if traversal_type == self.POSTORDER:
                yield curr_node

    # find_min travels across the leftChild of every node, and returns the
    # node who has no leftChild. This is the min value of a subtree
    def find_min(self):
        current_node = self.root
        while current_node.left:
            current_node = current_node.left
        return current_node

    # find_node expects a data and returns the Node object for the given data
    def find_node(self, data):
        if self.root:
            res = self.__get(data, self.root)
            if res:
                return res
            else:
                raise KeyError('Error, data not found')
        else:
            raise KeyError('Error, tree has no root')
    # helper function __get receives a data and a node. Returns the node with
    # the given data
    def __get(self, data, current_node):
        if current_node is self.sentinel: # if current_node does not exist return None
            print("couldnt find data: {}".format(data))
            return None
        elif current_node.data == data:
            return current_node
        elif data < current_node.data:
            # recursively call __get with data and current_node's left
            return self.__get( data, current_node.left )
        else: # data is greater than current_node.data
            # recursively call __get with data and current_node's right
            return self.__get( data, current_node.right )

    def find_successor(self, data):
        # Private Method, can only be used inside of BST.
        current_node = self.find_node(data)
        if current_node is self.sentinel:
            raise KeyError
        # Travel left down the rightmost subtree
        if current_node.right:
            current_node = current_node.right
            while current_node.left is not self.sentinel:
                current_node = current_node.left
            successor = current_node
        # Travel up until the node is a left child
        else:
            parent = current_node.parent
            while parent is not self.sentinel and current_node is not parent.left:
                current_node = parent
                parent = parent.parent
            successor = parent
        if successor:
            return successor
        else:
            return None

    # put adds a node to the tree
    def insert(self, data):
        # if the tree has a root
        if self.root:
            # use helper method __put to add the new node to the tree
            new_node = self.__put(data, self.root)
            self.__rb_insert_fixup(new_node)
        else: # there is no root
            # make root a Node with values passed to put
            self.root = Node(data, parent = self.sentinel, left = self.sentinel, right = self.sentinel)
            new_node = self.root
            self.__rb_insert_fixup(new_node)

    #Insertion for Binary Search Tree
    def bst_insert(self, data):
        # if the tree has a root
        if self.root:
            # use helper method __put to add the new node to the tree
            self.__put(data, self.root)
        else: # there is no root
            # make root a Node with values passed to put
            self.root = Node(data, parent = self.sentinel, left = self.sentinel, right = self.sentinel)

    # helper function __put finds the appropriate place to add a node in the tree
    def __put(self, data, current_node):
        if data < current_node.data:
            if current_node.left != self.sentinel:
                new_node = self.__put(data, current_node.left)
            else: # current_node has no child
                new_node = Node(data,
                parent = current_node,
                left = self.sentinel,
                right = self.sentinel )
                current_node.left = new_node
        else: # data is greater than or equal to current_node's data
            if current_node.right != self.sentinel:
                new_node = self.__put(data, current_node.right)
            else: # current_node has no right child
                new_node = Node(data,
                parent = current_node,
                left = self.sentinel,
                right = self.sentinel )
                current_node.right = new_node
        return new_node

    def delete(self, data):
        # Same as binary tree delete, except we call rb_delete fixup at the end.
        z = self.find_node(data)
        if z.left is self.sentinel or z.right is self.sentinel:
            y = z
        else:
            y = self.find_successor(z.data)
        
        if y.left is not self.sentinel:
            x = y.left
        else:
            x = y.right
        
        if x is not self.sentinel:
            x.parent = y.parent
        if y.parent is self.sentinel:
            self.root = x
        else:
            if y == y.parent.left:
                y.parent.left = x
            else:
                y.parent.right = x
        
        if y is not z:
            z.data = y.data
    
        if y.color == 'black':
            if x is self.sentinel:
                self.__rb_delete_fixup(y)
            else:
                self.__rb_delete_fixup(x)

    def left_rotate(self, current_node):
        """ 
        This function takes in a node object from the tree and performs a left rotation on it accordingly
        ...
        Parameters
        ----------
        current_node : node object
        ...
        Returns
        -------
        None
        """
        if self.root == None or current_node.data == None or current_node.right.data == None:
            raise KeyError

        y = current_node.right
        current_node.right = y.left

        if y.left:
            y.left.parent = current_node

        y.parent = current_node.parent  
        
        if current_node.parent.data == None: # current node was the root
            self.root = y
        elif current_node == current_node.parent.left: # current node was a left child
            current_node.parent.left = y
        else:
            current_node.parent.right = y
        
        y.left = current_node
        current_node.parent = y

    def right_rotate(self, current_node):
        """ 
        This function takes in a node object from the tree and performs a right rotation on it accordingly
        ...
        Parameters
        ----------
        current_node : node object
        ...
        Returns
        -------
        None
        """
        if self.root == None or current_node.data == None or current_node.left.data == None:
            raise KeyError

        y = current_node.left
        current_node.left = y.right

        if y.right:
            y.right.parent = current_node

        y.parent = current_node.parent
        
        if current_node.parent.data == None: # current node was the root
            self.root = y
        elif current_node == current_node.parent.left: # current node was a left child
            current_node.parent.left = y
        else:
            current_node.parent.right = y

        y.right = current_node
        current_node.parent = y  

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

    def __rb_insert_fixup(self, z):
        """ 
        This function takes in a node object that has just been added into the rb tree 
        and performs a set of operations in order to maintian red black tree properties
        ...
        Parameters
        ----------
        z : node object
        ...
        Returns
        -------
        None
        """
        # Case 1: z is is the root
        if z == self.root:
            self.root.color = "black"
            return 

        while z.parent.color == "red":
            uncle = self.__get_sibling(z.parent)
            # Case 2: uncle of z is red
            if uncle and uncle.color == "red":
                z.parent.color = "black"
                uncle.color = "black"
                z.parent.parent.color = "red"
                z = z.parent.parent

            # Case 3a: uncle of z is black and it forms a left side line
            elif self.__is_left_child(z) and self.__is_left_child(z.parent):
                z.parent.color = "black"
                z.parent.parent.color = "red"
                self.right_rotate(z.parent.parent)
            # Case 3a: uncle of z is black and it forms a right side line
            elif self.__is_left_child(z) == False and self.__is_left_child(z.parent) == False:
                z.parent.color = "black"
                z.parent.parent.color = "red"
                self.left_rotate(z.parent.parent)
            # Case 3b: uncle of z is black and it forms a left triangle
            elif self.__is_left_child(z) == False and self.__is_left_child(z.parent):
                z = z.parent
                self.left_rotate(z)
                z.parent.color = "black"
                z.parent.parent.color = "red"
                self.right_rotate(z.parent.parent)
            # Case 3b: uncle of z is black and it forms a right triangle
            elif self.__is_left_child(z) and self.__is_left_child(z.parent) == False:
                z = z.parent
                self.right_rotate(z)
                z.parent.color = "black"
                z.parent.parent.color = "red"
                self.left_rotate(z.parent.parent)

            if z == self.root:
                break

        self.root.color = "black"

    def __rb_delete_fixup(self, x):
        """ 
        This function takes in a node object that has just been moved in order to replace a node that has been deleted 
        and performs a set of operations in order to maintian red black tree properties
        ...
        Parameters
        ----------
        x : node object
        ...
        Returns
        -------
        None
        """
        while x != self.root and x.color == "black":
            s = self.__get_sibling(x)
            if self.__is_left_child(x): # x is a left child
                # Case 1: x's sibling is red
                if s.color == "red":
                    s.color = "black"
                    x.parent.color = "red"
                    self.left_rotate(x.parent)
                    s = x.parent.right
                # Case 2: x's sibling and both nephews are black
                if s.left.color == "black" and s.right.color == "black":
                    s.color = "red"
                    x = x.parent
                else:
                    # Case 3: x's sibling and right nephew is black and it's left nephew is red
                    if s.left.color == "red" and s.right.color == "black":
                        s.left.color = "black"
                        s.color = "red"
                        self.right_rotate(s)
                        s = x.parent.right
                    # Case 4: x's sibling is black and it's nephews are red
                    s.color = x.parent.color
                    x.parent.color = "black"
                    s.right.color = "black"
                    self.left_rotate(x.parent)
                    x = self.root
            else: # x is a right child
                if s.color == "red":
                    s.color = "black"
                    x.parent.color = "red"
                    self.right_rotate(x.parent)
                    s = x.parent.left
                # Case 2: x's sibling and both nephews are black
                if s.left.color == "black" and s.right.color == "black":
                    s.color = "red"
                    x = x.parent
                else:
                    # Case 3: x's sibling and left nephew is black and it's right nephew is red
                    if s.right.color == "red" and s.left.color == "black":
                        s.right.color = "black"
                        s.color = "red"
                        self.left_rotate(s)
                        s = x.parent.left
                    # Case 4: x's sibling is black and it's nephews are red
                    s.color = x.parent.color
                    x.parent.color = "black"
                    s.left.color = "black"
                    self.right_rotate(x.parent)
                    x = self.root
        x.color = "black"
            
