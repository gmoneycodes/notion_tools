import os
import re
import json
from rich import print as pretty_print
from utils import link2id, fetch_notion_data, dump_json
from process import parse_text
from process import add_text, add_eq_inline, add_eq_block, create_new_paragraph
from dotenv import load_dotenv
from notion_client import Client
from notion_client.api_endpoints import BlocksChildrenEndpoint

load_dotenv()

auth = os.getenv("NOTION_KEY")
def run():
    diagnose = True
    if diagnose:
        client = Client(auth=auth)
        link="https://www.notion.so/ruyoga/testing-9dc1cff1b6e14172ab35cb42a1b4bfda?pvs=4"
        page_id = link2id(link)
        data = fetch_notion_data (client=client, id=page_id)
        # dump_json(data)
        last_block_id = data['results'][-1].get('id')
        test_block = create_new_paragraph()
        add_text(test_block, "hellloooooooo mamamia lezatos")
        add_eq_inline(test_block, text="e = mc^2")
        pretty_print(test_block)

        example_str = r"""
        To solve this problem, we'll use the properties of a uniformly distributed discrete random variable. The probability of any one integer in this distribution is the same for all integers in the range \([a, b]\). That is, the probability of a single integer is \(\frac{1}{n}\), where \(n\) is the number of integers in the range.

We're given:

1. \(P(3 \leq X \leq 7) = \frac{1}{21}\)
2. \(P(0 \leq X \leq 5) = \frac{1}{35}\)

We can use these probabilities to determine the total number of integers in the range \([a, b]\).

For the range \([3, 7]\), there are \(7 - 3 + 1 = 5\) integers, so the probability for each integer is \( \frac{1}{21} \), and the total number of integers in the range \([a, b]\) should be \(21\).

For the range \([0, 5]\), there are \(5 - 0 + 1 = 6\) integers, so the probability for each integer is \( \frac{1}{35} \), and the total number of integers in the range \([a, b]\) should be \(35\).

But since \(a \leq 3\) and \(b \geq 10\), the total number of integers should be the same in both cases, which indicates a discrepancy between the two pieces of information given.

Let's find a common multiple of \(21\) and \(35\) that could represent the total number of integers, which would reconcile the two pieces of information. The least common multiple of \(21\) and \(35\) is \(105\), suggesting that there might be \(105\) integers in the range \([a, b]\).

This leads to a probability of \( \frac{1}{105} \) for each integer.

Now, we need to find \(P(90 \leq X \leq 110)\), given that the range of \(X\) includes at least the integers from \(3\) to \(10\). If \(105\) is the total number of integers from \(a\) to \(b\), and since \(90\) and \(110\) are outside the possible range of \(X\) (because \(b\) is at least \(10\)), the probability of \(X\) being between \(90\) and \(110\) is \(0\).

Thus, \(P(90 \leq X \leq 110) = 0\) under the given constraints.
        """
        str_array = parse_text(example_str)

        def str2json(str_array):
            re_parentheses = r'^\\\(.*?\\\)$'
            re_sqbrackets = r'^\\\[.*?\\\]$'

            output_json = create_new_paragraph()
            for idx, strs in enumerate(str_array):
                if re.match(re_parentheses, strs):
                    add_eq_inline(output_json, strs)
                elif re.match(re_sqbrackets, strs):
                    add_eq_block(output_json, strs)
                else:
                    add_text(output_json, strs)
            return output_json
        pretty_print(str_array)
        out = str2json(str_array)
        pretty_print(out)
        client.blocks.children.append(last_block_id, children=out)



    # Append the content to the block
    #client.blocks.children.append(last_block_id, children=test_block)
    #client.blocks.children.append(last_block_id, children=children_blocks)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    run()