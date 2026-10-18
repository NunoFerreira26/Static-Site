import unittest
from htmlnode import HTMLnode,ParentNode,LeafNode
from textnode import TextNode,TextType,text_node_to_html_node
from split_nodes_delimiter import split_nodes_delimiter,extract_markdown_images,extract_markdown_links,split_nodes_image,split_nodes_links,text_to_textnodes,markdown_to_html_node,extract_title

class TestTextNode(unittest.TestCase):
    """
    def test_eq(self): #If tests are equal
        node = HTMLnode("p", "This is a text HTML node", [HTMLnode("h1", "Title"), HTMLnode("h2", "Subtitle")], {"href": "https://www.google.com",
    "target": "_blank",})
        node2 = HTMLnode("p", "This is a text HTML node", [HTMLnode("h1", "Title"), HTMLnode("h2", "Subtitle")], {"href": "https://www.google.com",
    "target": "_blank",})
        self.assertEqual(node, node2)
    def test_eq1(self): #If tags are different
        node = HTMLnode("p", "This is a text HTML node", [HTMLnode("h1", "Title"), HTMLnode("h2", "Subtitle")], {"href": "https://www.google.com",
    "target": "_blank",})
        node2 = HTMLnode("a", "This is a text HTML node", [HTMLnode("h1", "Title"), HTMLnode("h2", "Subtitle")], {"href": "https://www.google.com",
    "target": "_blank",})
        self.assertNotEqual(node, node2)
    def test_eq2(self): #If values are different
        node = HTMLnode("p", "This is a text HTML node", [HTMLnode("h1", "Title"), HTMLnode("h2", "Subtitle")], {"href": "https://www.google.com",
    "target": "_blank",})
        node2 = HTMLnode("p", "This is not a text HTML node", [HTMLnode("h1", "Title"), HTMLnode("h2", "Subtitle")], {"href": "https://www.google.com",
    "target": "_blank",})
        self.assertNotEqual(node, node2)
    def test_eq3(self): #If children are different
        node = HTMLnode("p", "This is a text HTML node", [HTMLnode("h1", "Title"), HTMLnode("h2", "Subtitle")], {"href": "https://www.google.com",
    "target": "_blank",})
        node2 = HTMLnode("p", "This is a text HTML node", [HTMLnode("h1", "Title"), HTMLnode("h3", "Subsubtitle")], {"href": "https://www.google.com",
    "target": "_blank",})
        self.assertNotEqual(node, node2)
    def test_eq4(self): #If props are different
        node = HTMLnode("p", "This is a text HTML node", [HTMLnode("h1", "Title"), HTMLnode("h2", "Subtitle")], {"href": "https://www.google.com",
    "target": "_blank",})
        node2 = HTMLnode("p", "This is a text HTML node", [HTMLnode("h1", "Title"), HTMLnode("h2", "Subtitle")], {})
        self.assertNotEqual(node, node2)
    def test_props_to_html(self): #If model props_to_html does return http link correclty
        node = HTMLnode(
            "a",
            "Click",
            props={"href": "https://google.com", "target": "_blank"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' href="https://google.com" target="_blank"',
        )
    
    def test_leaf_to_html_p(self): #If the children are the same
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    def test_leaf_to_html_s(self): #If the url is correctly
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')
    def test_leaf_to_html_t(self): #If tag is None
        node = LeafNode(None, "Click me!", None)
        self.assertEqual(node.to_html(), "Click me!")
    def test_leaf_to_html_q(self): #If tag is None
        node = LeafNode(None, None, None)
        with self.assertRaises(ValueError) as cm:
            node.to_html()
        self.assertEqual(str(cm.exception), "All leaf nodes must have a value.")
    
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")
    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    def test_to_html_without_childern(self):
        Parent_node = ParentNode("p",[])
        with self.assertRaises(ValueError) as cm:
            Parent_node.to_html()
        self.assertEqual(str(cm.exception),"All parent nodes have children.")
    def test_to_html_without_tags(self):
        child_node = LeafNode("b", "child")
        Parent_node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError) as cm:
            Parent_node.to_html()
        self.assertEqual(str(cm.exception),"All parent nodes must have a tag.")
    def test_parent_with_props(self):
        node = ParentNode("div",[LeafNode("p", "Hello")],props={"class": "container", "id": "main"})
        self.assertEqual(node.to_html(),'<div class="container" id="main"><p>Hello</p></div>')
    def test_multiple_children(self):
        node = ParentNode("p",[LeafNode("b", "Bold"),LeafNode(None, " and "),LeafNode("i", "italic"),])
        self.assertEqual(node.to_html(), "<p><b>Bold</b> and <i>italic</i></p>")
    
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    def test_bold(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")
    def test_italic(self):
        node = TextNode("This is an italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic node")
    def test_code(self):
        node = TextNode("print('Hellow World')", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('Hellow World')")
    def test_link(self):
        node = TextNode("Click me!", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click me!")
        self.assertEqual(html_node.props, {"href":"https://www.google.com"})
    def test_image(self):
        node = TextNode("Image here!", TextType.IMAGE, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src":"https://www.google.com","alt":"Image here!"})
    def test_exception(self):
        node = TextNode("Image here!", "url", "https://www.google.com")
        with self.assertRaises(Exception) as cm:
            text_node_to_html_node(node)
        self.assertEqual(str(cm.exception), "TextType invalid. Please choose one of the following: text, bold, italic, code, link, image")
    
    def test_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("This is text with a ", TextType.TEXT),TextNode("code block", TextType.CODE),TextNode(" word", TextType.TEXT),])
    def test_bold(self):
        node = TextNode("This is text with a **bold block** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [TextNode("This is text with a ", TextType.TEXT),TextNode("bold block", TextType.BOLD),TextNode(" word", TextType.TEXT),])
    def test_italic(self):
        node = TextNode("This is text with a _italic block_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes, [TextNode("This is text with a ", TextType.TEXT),TextNode("italic block", TextType.ITALIC),TextNode(" word", TextType.TEXT),])
    def test_Type_Text(self):
        node = TextNode("`code block`", TextType.CODE)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("`code block`", TextType.CODE),])
    def test_delimeter(self):
        node = TextNode("This is text with a *code block* word", TextType.TEXT)
        with self.assertRaises(Exception) as cm:
            split_nodes_delimiter([node], "*", TextType.CODE)
        self.assertEqual(str(cm.exception), "Invalid Markdown syntax!")
    def test_unclosed_delimeter(self):
        node = TextNode("This is text with a **code block word", TextType.TEXT)
        with self.assertRaises(Exception) as cm:
            split_nodes_delimiter([node], "**", TextType.CODE)
        self.assertEqual(str(cm.exception), "Unclosed Delimeter!")
    
    def test_markdown_images(self):
        image = extract_markdown_images("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")
        self.assertEqual(image, [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])
    def test_markdown_images1(self):
            image = extract_markdown_images("This is text with a ![](https://i.imgur.com/aKaOqIh.gif)")
            self.assertEqual(image, [("", "https://i.imgur.com/aKaOqIh.gif")])
    def test_markdown_images_2(self):
        with self.assertRaises(Exception) as cm:
            extract_markdown_images("This is text with a ![rick roll(https://i.imgur.com/aKaOqIh.gif)")
        self.assertEqual(str(cm.exception), "Wrong markdown image regex! Correct: ![alt_text](url)")
    def test_markdown_images_3(self):
        with self.assertRaises(Exception) as cm:
            extract_markdown_images("")
        self.assertEqual(str(cm.exception), "Empty string")
    def test_markdown_links(self):
        image = extract_markdown_links("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")
        self.assertEqual(image, [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])
    
    def test_split_images(self):
        node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )
    def test_split_images_1(self):
        node = TextNode(
        "![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                #TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )
    def test_split_images_2(self):
        node = TextNode(
        "![image](https://i.imgur.com/zjjcJKZ.png) ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                #TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )
    def test_split_images_3(self):
        node = TextNode(
        "![image](https://i.imgur.com/zjjcJKZ.png) This is text with an",
        TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                #TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" This is text with an", TextType.TEXT),
                #TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )
    def test_split_images_4(self):
        node = TextNode(
        "This is text with an [image](https://i.imgur.com/zjjcJKZ.png) and another [second image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an [image](https://i.imgur.com/zjjcJKZ.png) and another [second image](https://i.imgur.com/3elNhQu.png)", TextType.TEXT),
                #TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                #TextNode(" This is text with an", TextType.TEXT),
                #TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )
    def test_split_links(self):
        node = TextNode(
        "This is text with a link [to boot dev](https://www.boot.dev) and another [to youtube](https://www.youtube.com/@bootdotdev)",
        TextType.TEXT,
        )
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ],
            new_nodes,
        )  
    def test_split_links_1(self):
        node = TextNode(
        "This is text with a link ![to boot dev](https://www.boot.dev) and another ![to youtube](https://www.youtube.com/@bootdotdev)",
        TextType.TEXT,
        )
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ![to boot dev](https://www.boot.dev) and another ![to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT),
            ],
            new_nodes,
        )
    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes,
        )
    def test_text_to_textnodes_1(self):
        text = "[link](https://boot.dev) This is _italic_ with an **text** word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" This is ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" with an ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a", TextType.TEXT),
            ],
            new_nodes,
        )
    """
    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
    def test_heading(self):
        md = "# Hellow World!"
        node = extract_title(md)
        self.assertEqual(
            node,"Hellow World!"
        )
if __name__ == "__main__":
    unittest.main()