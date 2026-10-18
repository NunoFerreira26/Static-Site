from textnode import TextNode,TextType, text_node_to_html_node
from htmlnode import HTMLnode, ParentNode
from enum import Enum
import re

class Delimiter(Enum):
    BOLD = "**"
    ITALIC = "_"
    CODE = "`"

class BlockType(Enum):
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNOREDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"
    PARAGRAPH = "paragraph"

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    if delimiter not in [d.value for d in Delimiter]: #Validate delimiter
        raise Exception("Invalid Markdown syntax!")

    new_list = []

    for i in range(len(old_nodes)):
        if old_nodes[i].text_type != TextType.TEXT: #Non-Text nodes (already converted nodes) pass through untouched
            new_list.append(old_nodes[i])
            continue
        else:
            split_string = old_nodes[i].text.split(delimiter)
            if len(split_string) % 2 == 0: #If the lenght of the array is not odd, then it's delimiter is not closed
                raise Exception("Unclosed Delimeter!")
            for j in range(len(split_string)):
                if j % 2 != 0:
                    new_list.append(TextNode(split_string[j], text_type))
                else:
                    new_list.append(TextNode(split_string[j], TextType.TEXT))
    return new_list

def extract_markdown_images(text:str|None=None) -> list[tuple[str,str]]:
    if not text: #Verifies if the text string is empty
        raise Exception("Empty string")
    pattern = r"!\[([^\[\]]*)\]\(([^()]*)\)"
    new_list = re.findall(pattern, text)
    #if new_list == []:
        # raise Exception("Wrong markdown image regex! Correct: ![alt_text](url)")
    return new_list
    #!\[ - Matches the literal ![ starting an image
    #([^\[\]]*) - Matches any sequence of characters inside [...]
    #\]\( - Matches the literal ]( seperator between alt text and URL
    #([^()]*) - Matches any sequence of characters inside (...)
    #\) - Matches the closing parenthesis )

def extract_markdown_links(text:str|None=None) -> list[tuple[str,str]]:
    if not text: #Verifies if the text string is empty
        raise Exception("Empty string")
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    new_list = re.findall(pattern, text)
    #if new_list == []:
        #raise Exception("Wrong markdown url regex! Correct: [alt_text](url)")
    return new_list

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_node = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT: #Non-Text nodes (already converted nodes) pass through untouched
            new_node.append(node)
            continue
        image_markdown = extract_markdown_images(node.text) #List of tuples [(alt tex, url),]
        read = node.text
        if image_markdown == []:
            new_node.append(TextNode(read,TextType.TEXT))
        else:
            for alt_text, url in image_markdown:
                i = 0 #Tells me on what image is at
                link_mardown = f"![{alt_text}]({url})"
                sections = read.split(link_mardown,1)
                if sections[0] != "": #We know that text precedes the image
                    new_node.append(TextNode(sections[0],TextType.TEXT))
                new_node.append(TextNode(alt_text,TextType.IMAGE,url))
                if sections[1] != "":
                    if i != (len(image_markdown) - 1):
                        read = sections[1] #This way it only reads what is after the first image alt_text and url
                    else:
                        new_node.append(TextNode(sections[1],TextType.TEXT))
                i += 1
    return new_node  

def split_nodes_links(old_nodes: list[TextNode]) -> list[TextNode]:
    new_node = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT: #Non-Text nodes (already converted nodes) pass through untouched
            new_node.append(node)
            continue
        link_markdown = extract_markdown_links(node.text) #List of tuples [(alt tex, url),]
        read = node.text
        if link_markdown == []:
            new_node.append(TextNode(read,TextType.TEXT))
        else:
            for alt_text, url in link_markdown:
                i = 0 #Tells me on what image is at
                link_mardown = f"[{alt_text}]({url})"
                sections = read.split(link_mardown,1) #Get a list with strings before and fater the markdown link 
                if sections[0] != "": #We know that text precedes the link
                    new_node.append(TextNode(sections[0],TextType.TEXT))
                new_node.append(TextNode(alt_text,TextType.LINK,url))
                if sections[1] != "":
                    if i != (len(link_markdown) - 1): #See if it's the last link_mardown
                        read = sections[1] #This way it only reads what is after the first link alt_text and url
                    else:
                        new_node.append(TextNode(sections[1],TextType.TEXT))
                i += 1
    return new_node

def text_to_textnodes(text:str|None=None) -> list[TextNode]:
    text_nodes = []
    text_nodes.append(TextNode(text, TextType.TEXT))

    first = split_nodes_image(text_nodes)
    second = split_nodes_links(first)
    thrid = split_nodes_delimiter(second,'**',TextType.BOLD)
    fourth = split_nodes_delimiter(thrid,'`',TextType.CODE)
    fifth = split_nodes_delimiter(fourth,'_',TextType.ITALIC)

    return fifth

def markdown_to_blocks(markdown:str|None=None) -> list[str]:
    cleaned_markdown = markdown.strip().strip('"""').strip("'''").strip()
    blocks = cleaned_markdown.split("\n\n") #Split string based on it's delimiter
    for i in range(len(blocks)):
        blocks[i] = blocks[i].strip() #Strip any leading or trailing whitespace from each block
        if blocks[i] == "":
            blocks.pop(i) #Remove any empty blocks due to excessive newlines
    return blocks

def block_to_block_type(block:str|None=None) -> BlockType:
    if block.startswith(("#", "##", "###", "####", "#####", "######")):
        return BlockType.HEADING

    lines = block.split("\n")
    if len(lines) > 1 and block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNOREDERED_LIST
    is_ordered = True
    for i, line in enumerate(lines, start=1):
        if not line.startswith(f"{i}. "):
            is_ordered = False
            break
    if is_ordered and len(lines)>0:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown: str|None=None) -> HTMLnode:
    #Split the markdown into blocks
    list_blocks = markdown_to_blocks(markdown)
    block_nodes = []

    for block in list_blocks: #Loop over each block
        block_type = block_to_block_type(block) #Determine the type block
        html_node = block_to_html_node(block, block_type)
        block_nodes.append(html_node)
    return ParentNode("div", children=block_nodes)

def text_to_children(text: str) -> list[HTMLnode]:
    """Helper: Converts inline markdown string into a list of HTMLNodes."""
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def block_to_html_node(block: str, block_type: BlockType) -> HTMLnode:
    match block_type:
        case BlockType.PARAGRAPH:
            # Paragraphs can be multiline; join lines with spaces
            lines = block.split("\n")
            paragraph_text = " ".join(line.strip() for line in lines if line.strip())
            children = text_to_children(paragraph_text)
            return ParentNode("p", children)

        case BlockType.HEADING:
            # Determine heading level by counting leading '#'
            level = 0
            for char in block:
                if char == "#" and level<7:
                    level += 1
                else:
                    break
            # Remove heading prefix (e.g., '## ')
            text = block[level + 1 :]
            children = text_to_children(text)
            return ParentNode(f"h{level}", children)

        case BlockType.CODE:
            # Code blocks do NOT parse inline markdown
            # Strip outer ``` ticks and optional trailing newline
            if block.startswith("```") and block.endswith("```"):
                content = block[3:-3]
            else:
                content = block

            lines = content.split("\n")
            cleaned_lines = [line.strip() for line in lines if line.strip() != ""]
            content = "\n".join(cleaned_lines) + "\n"

            text_node = TextNode(content, TextType.TEXT)
            code_node = ParentNode("code", [text_node_to_html_node(text_node)])
            return ParentNode("pre", [code_node])

        case BlockType.QUOTE:
            # Strip '>' from each line and join them
            lines = block.split("\n")
            new_lines = []
            for line in lines:
                if line.startswith(">"):
                    # Strip leading '>' and optional space
                    line = line[1:].lstrip(" ")
                new_lines.append(line)
            content = " ".join(new_lines)
            children = text_to_children(content)
            return ParentNode("blockquote", children)

        case BlockType.UNOREDERED_LIST:
            lines = block.split("\n")
            items = []
            for line in lines:
                # Strip leading '- ' or '* '
                text = line[2:]
                children = text_to_children(text)
                items.append(ParentNode("li", children))
            return ParentNode("ul", items)

        case BlockType.ORDERED_LIST:
            lines = block.split("\n")
            items = []
            for line in lines:
                # Strip leading '1. ', '2. ', etc.
                text = line.split(". ", 1)[1]
                children = text_to_children(text)
                items.append(ParentNode("li", children))
            return ParentNode("ol", items)

        case _:
            raise ValueError(f"Invalid block type: {block_type}")

def extract_title(markdown:str|None=None) -> str:
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("No Header found in markdown.")