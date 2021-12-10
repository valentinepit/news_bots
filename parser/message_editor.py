def create_message(message):
    result = f"<b>{message['title']}</b>\n{message['text']}\n{message['source']}"
    # result = f"*{message['title']}*\n{message['text']}\n{message['source']}"

    for tag in message["tags"]:
        result += f"{tag}\n"
    return result


def convert_row_news(_news):
    source = f"{_news['Source']['url']}\n"
    title = f"{_news['Name']['title'][0]['text']['content']}\n"
    text = text_editor(_news["Notes"]["rich_text"]) + "\n"
    public_time = _news["Date to publish"]["date"]["start"]
    tags = _news["#"]["rich_text"][0]["plain_text"].split("\n")
    return {"title": title, "source": source, "text": text, "time": public_time, "tags": tags}


def text_editor(data):
    result = ''
    for i in range(len(data)):
        if not data[i]["text"]["link"]:
            temp = data[i]["text"]["content"]
            if data[i]["annotations"]["bold"]:
                temp = f"<b>{temp}</b>"
            if data[i]["annotations"]["italic"]:
                temp = f"<i>{temp}</i>"
            if data[i]["annotations"]["strikethrough"]:
                temp = f"<s>{temp}</s>"
            if data[i]["annotations"]["underline"]:
                temp = f"<u>{temp}</u>"
            if data[i]["annotations"]["color"] != "default":
                temp = f'<span style="color:{data[i]["annotations"]["color"]}">{temp}</span>'
            result = result + temp
        else:
            result = result + f'<a href=\"{data[i]["text"]["link"]["url"]}\">' \
                              f'{data[i]["text"]["content"]}</a>'

    return result

# def text_editor(data):
#     result = ''
#     for i in range(len(data)):
#         if not data[i]["text"]["link"]:
#             temp = data[i]["text"]["content"]
#             if data[i]["annotations"]["bold"]:
#                 temp = f"*{temp}*"
#             if data[i]["annotations"]["italic"]:
#                 temp = f"_{temp}_"
#             if data[i]["annotations"]["strikethrough"]:
#                 temp = f"~{temp}~"
#             if data[i]["annotations"]["underline"]:
#                 temp = f"__{temp}__"
#             # if data[i]["annotations"]["color"] != "default":
#             #     temp = f'<span style="color:{data[i]["annotations"]["color"]}">{temp}</span>'
#             result = result + temp
#         else:
#             result = result + f'[inline URL]({data[i]["text"]["link"]["url"]})' \
#                               f'{data[i]["text"]["content"]}'
#
#     return result
