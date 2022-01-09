import re

tag_pattern = r"(@[a-z]*\W)(.*)"
channel_pattern = r"(<#[\d]*>)"


def convert_row_news(msg, source_id):
    links = re.findall(channel_pattern, msg)
    for link in links:
        msg = msg.replace(link, change_channel_link(link, source_id))
    if msg.startswith("@"):
        msg = delete_tags(msg)
    return msg


def delete_tags(msg_text):
    return re.match(tag_pattern, msg_text)[2]


def change_channel_link(_link, _id):
    result = "https://discord.com/channels/" + _id + "/" + _link.lstrip("<#").rstrip(">")
    return result
