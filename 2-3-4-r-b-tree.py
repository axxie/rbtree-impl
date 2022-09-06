from random import randrange

class TwoThreeNode:
    def __init__(self, value):
        self.values = [value]
        self.children = [None, None]

    def __repr__(self) -> str:
        return "Node: " + str(self.values)

    def add_to_leaf(self, value):
        self.values.append(value)
        self.values.sort()
        self.children.append(None)

    def add_to_inner(self, i, value, right):
        if value is None:
            return

        self.values[i:i] = [value]
        self.children[i+1:i+1] = [right]

    def is2(self):
        return len(self.values) == 1

    def extract_middle_value(self):
        assert len(self.values) == 3
        value = self.values[1]

        other = TwoThreeNode(self.values[2])
        other.children = self.children[2:4]

        self.values=[self.values[0]]
        self.children = self.children[0:2]

        return value, other


class TwoThreeTree:
    def __init__(self):
        self.root = None

    def add(self, value):
        if self.root is None:
            self.root = TwoThreeNode(value)
            return

        new_value, new_right = self.add_internal(self.root, value)
        if new_value is None:
            return

        new_root = TwoThreeNode(new_value)
        new_root.children[0] = self.root
        new_root.children[1] = new_right

        self.root = new_root

    def insert_into_values(self, node, value):
        for i in range(len(node.values) + 1):

            if i == len(node.values) or value < node.values[i]:
                new_value, new_right = self.add_internal(node.children[i], value)
                node.add_to_inner(i, new_value, new_right)
                break
            elif value == node.values[i]:
                break

    def add_internal(self, node, value):

        if node is None:
            return value, None

        self.insert_into_values(node, value)

        if len(node.values) > 2:
            return node.extract_middle_value()

        return None, None

    def __repr__(self) -> str:
        return self.repr_internal(self.root)

    def repr_internal(self, node):
        if node.children[0] is None:
            return "[" + str(node) + "]\n"

        result = str(node) + " -> " + str(node.children[0]) + "\n"
        result = result + str(node) + " -> " + str(node.children[1]) + "\n" # right in case of 2-node and middle in case of 3-node

        if not node.is2():
            result = result + str(node) + " -> " + str(node.children[2]) + "\n"

        result = result + self.repr_internal(node.children[0])
        result = result + self.repr_internal(node.children[1])

        if not node.is2():
            result = result + self.repr_internal(node.children[2])


        return result

    def get_as_set(self):
        result = set()
        self.get_as_set_internal(result, self.root)
        return result

    def get_as_set_internal(self, result, node):
        if node is None:
            return

        result.update(node.values)
        for child in node.children:
            self.get_as_set_internal(result, child)


class RBTreeNode:
    RED = 1
    BLACK = 2

    def __init__(self, value):
        self.value = value
        self.children = [None, None]
        self.color = RBTreeNode.RED

    def __repr__(self) -> str:
        color = "R" if self.color == RBTreeNode.RED else "B"
        return "Node: " + color + " " + str(self.value)


class RBTree:
    def __init__(self):
        self.root = None

    def add(self, value):
        if self.root is None:
            self.root = RBTreeNode(value)
            self.root.color = RBTreeNode.BLACK
            return


        stack = []
        parent = None
        current = self.root
        while current is not None:
            parent = current
            if value < current.value:
                current = current.children[0]
                child_index = 0
            elif value > current.value:
                current = current.children[1]
                child_index = 1
            else:
                return

            stack.append((parent, child_index))

        stack.pop()
        parent.children[child_index] = RBTreeNode(value)
        while parent.color == RBTreeNode.RED:
            if self.root == parent:
                self.root.color = RBTreeNode.BLACK
                return

            grand_parent, grand_child_index = stack.pop()
            if grand_parent.children[1 - grand_child_index].color == RBTreeNode.RED:
                grand_parent.children[0].color = RBTreeNode.BLACK
                grand_parent.children[1].color = RBTreeNode.BLACK
                grand_parent.color = RBTreeNode.RED
                parent = grand_parent
                child_index = grand_child_index

    def __repr__(self) -> str:
        return self.repr_internal(self.root)

    def repr_internal(self, node):
        result = ""
        if node.children[0]:
            result = result + str(node) + " -> " + str(node.children[0]) + "\n"
        if node.children[1]:
            result = result + str(node) + " -> " + str(node.children[1]) + "\n"

        if node.children[0]:
            result = result + self.repr_internal(node.children[0])
        if node.children[1]:
            result = result + self.repr_internal(node.children[1])
        return result


def test_instance(items):
    correct = set()
    to_check = TwoThreeTree()
    for x in items:
        correct.add(x)
        to_check.add(x)
        assert correct == to_check.get_as_set()

    # print(to_check)


def test():
    test_instance(range(10))
    test_instance(range(10,0, -1))
    test_instance(range(100))
    for r in range(20):
        test_instance([randrange(100) for x in range(1000)])


t = RBTree()
t.add(10)
t.add(5)
t.add(15)
t.add(3)
t.add(7)
t.add(12)
t.add(17)
t.add(1)
print(t)
