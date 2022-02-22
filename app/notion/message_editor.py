import json
from datetime import datetime
from typing import Dict, List


def create_message(message):
    msg_text = f"<b>{message['title']}</b>" f"\n{message['text']}\n{message['source']}\n"
    for tag in message["tags"]:
        msg_text += f"{tag}\n"

    return {"text": msg_text, "photo": message["picture"]}


def convert_row_news(_news):
    source = f"{_news['Source']['url']}\n" if _news["Source"]["url"] else ""
    public_time = _news["Date to publish"]["date"]["start"] if _news["Date to publish"]["date"] else datetime.now()
    text = add_tags_to_text(_news["Notes"]["rich_text"]) + "\n" if _news["Notes"]["rich_text"] != [] else ""
    title = f"{_news['Name']['title'][0]['text']['content']}\n" if _news["Name"]["title"] else ""
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


def create_page_content(source, _data) -> Dict:
    payload = json.loads(open("notion/schema.json", "r").read())
    fields = payload["properties"]
    fields["Source"]["url"] = source
    fields["Date"]["date"]["start"] = _data["date"].replace(".", "-")
    fields["Name"]["title"][0]["text"]["content"] = _data["header"]
    fields["Notes"]["rich_text"][0]["text"]["content"] = (
        f"{_data['content']}\n"
        f"Amount of loss: {_data['amount_of_loss']}\n"
        f"Attack method: {_data['attack_method']}"
    )
    return payload
