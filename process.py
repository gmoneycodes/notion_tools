import re
from utils import clean_latex


def create_new_paragraph():
    return [{
        "object": "block",
        "paragraph": {
           "rich_text": []
        }
    }]


def add_text(json_data, text):
    json_data[0]['paragraph']['rich_text'].append({
        "type": "text",
        "text": {
            "content": text
        }
    })


def add_eq_inline(json_data, text):
    json_data[0]['paragraph']['rich_text'].append({
        "type": "equation",
        "equation": {
            "expression": clean_latex(text)
        }
    })


def add_eq_block(json_data, text):
    return {
        "object": "block",
        "type": "equation",
        "equation": {
            "expression": clean_latex(text)
        }
    }



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