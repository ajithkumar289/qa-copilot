import json


def parse_testcases(response_text: str):

    try:
        return json.loads(response_text)

    except json.JSONDecodeError:
        return []