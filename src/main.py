from textnode import TextNode, TextType

def main():
    example = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(example)
    

main()