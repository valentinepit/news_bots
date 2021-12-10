from notion.client import NotionClient
from pprint import pprint

# token_v2 = "f3c7d2fc374e1715a06bced444d6a482c9374fc63cd019499d31fa469bae25d6f5d322372aff964df9b642061288bd1a5c586c0e20c456377448a82790ba22c23dfddbfb69a1632320daa0ae4f80"
# url = "https://www.notion.so/9404aafb375a4132b9a10d069a2ac580?v=128a5260b1424a7b8ea9ee23fddc1df8"
# DB_ID = "9404aafb375a4132b9a10d069a2ac580"
# client = NotionClient(token_v2=token_v2)
# cv = client.get_collection_view(url)

NOTION = "https://www.notion.so/warpis/News-beta-797640552fc24793b6b14465ac34118b"
TOKEN = "f3c7d2fc374e1715a06bced444d6a482c9374fc63cd019499d31fa469bae25d6f5d322372aff964df9b642061288bd1a5c586c0e20c456377448a82790ba22c23dfddbfb69a1632320daa0ae4f80"
client = NotionClient(token_v2=TOKEN)
cv = client.get_collection_view(NOTION)


# Replace this URL with the URL of the page you want to edit
# page = client.get_block(url)

print()