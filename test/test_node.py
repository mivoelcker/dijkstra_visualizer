import unittest

from model.Node import Node


class NodeTest(unittest.TestCase):

    def test_is_position_in_node(self):
        Node.radius = 10
        node = Node("A", 50, 50)
        self.assertEqual(True, node.is_position_in_node(50, 50))
        self.assertEqual(True, node.is_position_in_node(60, 50))
        self.assertEqual(True, node.is_position_in_node(50, 60))
        self.assertEqual(True, node.is_position_in_node(57, 57))
        self.assertEqual(False, node.is_position_in_node(61, 50))
        self.assertEqual(False, node.is_position_in_node(50, 61))
        self.assertEqual(False, node.is_position_in_node(57, 58))


if __name__ == '__main__':
    unittest.main()
