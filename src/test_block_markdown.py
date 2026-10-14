import unittest
from block_markdown import markdown_to_blocks, block_to_block_type, BlockType

class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line



- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block(self):
        md = """
This is a normal paragraph

### this is a heading

####### this should be a normal paragraph

```
another code block
```

> this should be a 
>quote block

- un
- ordered
- list

1. ordered 
2. li
3. st
"""
        blocks = markdown_to_blocks(md)
        block_types = []
        for block in blocks:
            block_types.append(block_to_block_type(block))
        answer = [
            BlockType.PARAGRAPH,
            BlockType.HEADING,
            BlockType.PARAGRAPH,
            BlockType.CODE,
            BlockType.QUOTE,
            BlockType.U_LIST,
            BlockType.O_LIST,
        ]

        self.assertEqual(block_types, answer)