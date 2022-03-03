import logging
import os
import tweepy


logger = logging.getLogger(__name__)

auth = tweepy.OAuthHandler(os.environ["TWITTER_API_KEY"], os.environ["TWITTER_API_KEY_SECRET"])
auth.set_access_token(os.environ["TWITTER_ACCESS_TOKEN"], os.environ["TWITTER_ACCESS_TOKEN_SECRET"])

api = tweepy.API(auth, wait_on_rate_limit=True)

try:
    api.verify_credentials()
    logger.info("Authentication to Twitter OK")
except Exception as e:
    logger.info(f"{e} Error during authentication")


sources = {
    "nansen_alpha": None
}


def get_user_twits(user_id, since_id=None):
    msgs = []
    if not since_id:
        new_user_twits = api.user_timeline(screen_name=user_id, count=10)
    else:
        new_user_twits = api.user_timeline(screen_name=user_id, since_id=since_id)
    for twit in new_user_twits:
        msgs.append(f"{user_id}\n{twit.created_at}\n{twit.text}")
    _last_id = new_user_twits[0] if new_user_twits[0] else since_id
    return msgs, _last_id


def get_new_twits():
    messages = []
    for source, last_id in sources.items():
        new_messages, new_last_id = get_user_twits(source, last_id)
        messages += new_messages
        sources[source] = new_last_id
    return messages


# news = get_new_twits()

# try:
#     api.verify_credentials()
#     print("Authentication OK")
# except Exception as e:
#     print(f"{e} Error during authentication")
