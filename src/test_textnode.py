import unittest
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self): #If tests are equal
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    def test_eq1(self): #If tests are different (message)
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is not a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)
    def test_eq2(self): #If tests are different (TextType)
            node = TextNode("This is a text node", TextType.LINK)
            node2 = TextNode("This is not a text node", TextType.BOLD)
            self.assertNotEqual(node, node2)
    def test_eq3(self): #If tests are different (One message without link. None)
            node = TextNode("This is a text node", TextType.LINK)
            node2 = TextNode("This is a text node", TextType.LINK, "https://www.boot.dev")
            self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()