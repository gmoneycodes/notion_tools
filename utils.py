import subprocess
import os
from uuid import uuid4
import requests
import json
from notion_client import Client
from dotenv import load_dotenv


def link2id(link):
    """
    turns "https://www.notion.so/GRE-Quant-Hard-380c78c0e0f54565bdbdc4ccb079050d?pvs=4"
    into "380c78c0-e0f5-4565-bdbd-c4ccb079050d"
    :param link: notion link
    :return: page id
    """
    l = link.split("-")[-1].split("?")[0]
    indices = [8, 12, 16, 20]
    parts = [l[i:j] for i, j in zip([0] + indices, indices + [None])]
    return "-".join(parts)


def clean_newlines(text):
    invalid_strs = ["\n", "\n\n"]
    for invalid in invalid_strs:
        text = text.replace(invalid, "")
    return text


def clean_latex(text, copy: bool = False):
    """
    :param text: text containing latex notations (backslash parentheses or square brackets)
    :param copy: whether to copy the cleaned text into the clipboard
    :return: clean text compatible with katex
    """
    invalid_strs = [r"\(", r"\[", r"\)", r"\]"]
    for invalid in invalid_strs:
        text = text.replace(invalid, "")
    if copy:
        subprocess.run("pbcopy", text=True, input=text)
    else:
        return text

def fetch_notion_data(client, id):
    """
    :param id: block/page id
    :param client: client object from notion-client
    :return: json: json of the requested page
    """
    return client.blocks.children.list(block_id=id)

def get_last_block_id(json):
    return json['data'][-1].get('id')

def dump_json(data):
    id = uuid4()
    with open(f"{id}.json", 'w') as file:
        json.dump(data, file, indent=4, sort_keys=False)

def load_tokens():
    load_dotenv()
    v1 = os.getenv("NOTION_KEY")
    v2 = os.getenv("V2TOKEN")
    return v1, v2