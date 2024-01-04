import re
from utils import clean_latex


def create_new_paragraph():
    return [{
        "object": "block",
        "paragraph": {
           "rich_text": []
        }
    }]


def str2json(str_array, kind=None):

    re_parentheses = r'^\\\(.*?\\\)$'
    re_sqbrackets = r'^\\\[.*?\\\]$'

    toggle = kind is not None
    output_json = add_toggle(kind) if toggle else create_new_paragraph()

    for idx, strs in enumerate(str_array):
        if re.match(re_parentheses, strs):
            add_eq_inline(output_json, strs, toggle=toggle)
        elif re.match(re_sqbrackets, strs):
            add_eq_block(output_json, strs, toggle=toggle)
        else:
            add_text(output_json, strs, toggle=toggle)
    return output_json


def add_text(json_data, text, toggle: bool):
    if not toggle:
        json_data[0]['paragraph']['rich_text'].append({
            "type": "text",
            "text": {
                "content": text
            }
        })
    else:
        json_data[0]['heading_3']['children'][0]['paragraph']['rich_text'].append({
            "type": "text",
            "text": {
                "content": text
            }
        })


def add_toggle(kind: str):
    if kind.lower() == 'hint':
        return [{
            "object": 'block',
            "type": 'heading_3',
            "heading_3": {
                "rich_text": [{'type': 'text', "text": {'content': "Hint 🕵️‍♂️"}}],
                "children": [
                    {"object": "block",
                     "type": "paragraph",
                     "paragraph": {
                         'rich_text': []
                     }
                     }
                ]
            }
        }]
    elif kind.lower() == 'answer':
        return [{
            "object": 'block',
            "type": 'heading_3',
            "heading_3": {
                "rich_text": [{'type': 'text', "text": {'content': "Answer 🌟"}}],
                "children": [
                    {"object": "block",
                     "type": "paragraph",
                     "paragraph": {
                         'rich_text': []
                     }
                     }
                ]
            }
        }]


def add_eq_inline(json_data, text, toggle: bool):
    if not toggle:
        json_data[0]['paragraph']['rich_text'].append({
            "type": "equation",
            "equation": {
                "expression": clean_latex(text)
            }
        })
    else:
        json_data[0]['heading_3']['children'][0]['paragraph']['rich_text'].append({
            "type": "equation",
            "equation": {
                "expression": clean_latex(text)
            }
        })


def add_eq_block(json_data, text, toggle: bool):
    if not toggle:
        return {
            "object": "block",
            "type": "equation",
            "equation": {
                "expression": clean_latex(text)
            }
        }
    else:
        json_data[0]['heading_3']['children'][0]['paragraph']['rich_text'].append({
            "object": "block",
            "type": "equation",
            "equation": {
                "expression": clean_latex(text)
            }
        })






def parse_text(input_string):
    """
    :param input_string: text to parse
    :return: array of text; split into equation & paragraph sections
    """
    # Regular expression for both \[ \] and \( \) delimiters
    regex = r"\\\[.+?\\\]|\\\(.+?\\\)"

    # Find all occurrences of the delimited strings
    matches = re.findall(regex, input_string)

    # Split the string at each occurrence of the delimited strings
    split_strings = re.split(regex, input_string)

    # Combine the split strings with the matched strings to get the desired structure
    result = []
    for i in range(len(split_strings)):
        result.append(split_strings[i])  # Non-delimited string
        if i < len(matches):
            result.append(matches[i])  # Delimited string

    return result