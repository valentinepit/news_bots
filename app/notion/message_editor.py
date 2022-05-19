import json
from datetime import datetime
from typing import Dict, List


def create_message(message):
    msg_text = f"<b>{message['title']}</b>" f"\n{message['text']}\n{message['source']}\n"
    for tag in message["tags"]:
        msg_text += f"{tag}\n"

    return {"text": msg_text, "photo": message["picture"]}


def convert_row_news(_news):
    title = ""
    source = f"{_news['Source']['url']}\n" if _news["Source"]["url"] else ""
    public_time = _news["Date to publish"]["date"]["start"] if _news["Date to publish"]["date"] else datetime.now()
    text = add_tags_to_text(_news["Notes"]["rich_text"]) + "\n" if _news["Notes"]["rich_text"] != [] else ""
    if _news["Name"]["title"] and len(_news["Name"]["title"]) == 1:
        title = f"{_news['Name']['title'][0]['text']['content']}\n"
    elif len(_news["Name"]["title"]) > 1:
        for title_part in _news["Name"]["title"]:
            title += title_part["text"]["content"]
    tags = _news["#"]["rich_text"][0]["plain_text"].split("\n") if _news["#"]["rich_text"] != [] else ""
    try:
        picture = _news["Picture"]["files"][0]["file"]["url"] if _news["Picture"]["files"] != [] else False
    except KeyError:
        picture = _news["Picture"]["files"][0]["external"]["url"]
    return {"title": title, "source": source, "text": text, "time": public_time, "tags": tags, "picture": picture}


def add_tags_to_text(data):
    result = ""
    for item in data:
        if not item["text"]["link"]:
            temp = item["text"]["content"]
            if item["annotations"]["bold"]:
                temp = f"<b>{temp}</b>"
            if item["annotations"]["italic"]:
                temp = f"<i>{temp}</i>"
            if item["annotations"]["strikethrough"]:
                temp = f"<s>{temp}</s>"
            if item["annotations"]["underline"]:
                temp = f"<u>{temp}</u>"
            if item["annotations"]["color"] != "default":
                temp = f'<span style="color:' f'{item["annotations"]["color"]}">{temp}</span>'
            result = result + temp
        else:
            result = result + f'<a href="' f'{item["text"]["link"]["url"]}">' f'{item["text"]["content"]}</a>'

    return result


def message_cutter(max_length: int, message: str) -> List:
    messages = []
    while len(message) >= max_length:
        last_point_index = message[:max_length].rindex("\n") + 1
        messages.append(message[:last_point_index])
        message = message[last_point_index:]
    messages.append(message)
    return messages


def create_exploit_page(title, _data) -> Dict:
    payload = json.loads(open("notion/schema.json", "r").read())
    fields = payload["properties"]
    fields["Title"]["title"][0]["text"]["content"] = title
    fields["Date of exploit"]["date"]["start"] = _data["date"]

    losses = int(_data["amount_of_loss"][1::].replace(",", "")) if _data["amount_of_loss"].startswith("$") else 0
    fields["Losses"]["number"] = losses

    fields["Attack type"]["select"]["name"] = prepare_description(_data["attack_method"])
    fields["About defiyield"]["rich_text"][0]["text"]["content"] = prepare_description(_data["About (defiyield.app)"])
    fields["About slowmist"]["rich_text"][0]["text"]["content"] = prepare_description(_data["About (slowmist)"])

    fields["Source"]["rich_text"][0]["text"]["content"] = _data["source"]

    fields["Projects"]["relation"] = _data["projects"]
    fields["Blockchain"]["relation"] = _data["blockchain"]
    return payload


def create_project_page(_data):
    payload = json.loads(open("notion/projects_schema.json", "r").read())
    payload["properties"]["Name"]["title"][0]["text"]["content"] = _data["header"]
    payload["properties"]["Chain"]["relation"] = _data["blockchain"]
    return payload


def prepare_description(description):
    result = description if description else " "
    result = result if len(result) <= 2000 else result[::200]
    return result
