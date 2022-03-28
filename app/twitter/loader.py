import logging
import os

import tweepy
from tweepy.errors import TweepyException, Unauthorized

logger = logging.getLogger(__name__)


class TwitterNews:
    sources = {
        "nansen_alpha": None,
        "0x_b1": None,
        "CurveCap": None,
        "crypto_condom": None,
        "VotiumProtocol": None,
        "Tetranode": None,
        "samkazemian": None,
        "DefiDividends": None,
        "CurveFinance": None,
        "samczsun": None,
    }
    api = None

    def get_api(self):
        auth = tweepy.OAuthHandler(os.environ["TWITTER_API_KEY"], os.environ["TWITTER_API_KEY_SECRET"])
        auth.set_access_token(os.environ["TWITTER_ACCESS_TOKEN"], os.environ["TWITTER_ACCESS_TOKEN_SECRET"])

        api = tweepy.API(auth, wait_on_rate_limit=True)

        try:
            api.verify_credentials()
            logger.info("Authentication to Twitter OK")
        except Exception as e:
            logger.info(f"{e} Error during authentication")
            return None
        return api

    def get_user_twits(self, user_id, since_id=None):
        msgs = []
        logger.info(f"uploading twits from {user_id}")
        if not since_id:
            try:
                new_user_twits = self.api.user_timeline(screen_name=user_id, count=1)
            except Unauthorized:
                logger.info(f"can't get twits from {user_id}")
                msgs.append(f"BAD_CHANNEL {user_id}")
                return msgs, since_id
        else:
            new_user_twits = self.api.user_timeline(screen_name=user_id, since_id=since_id)
        for twit in new_user_twits:
            msgs.append(f"<b>{user_id}</b>\n{twit.created_at}\n\n{twit.text}")
        try:
            _last_id = new_user_twits[0].id
        except IndexError:
            _last_id = since_id
        return msgs, _last_id

    def update_news(self):
        self.api = self.get_api()
        messages = []
        if not self.api:
            return messages
        for source, last_id in self.sources.items():
            try:
                new_messages, new_last_id = self.get_user_twits(source, last_id)
                self.sources[source] = new_last_id
                messages += new_messages
            except TweepyException:
                logger.info("Can't connect to Twitter user")

        for msg in messages:
            if msg.startswith("BAD_CHANNEL"):
                self.sources.pop(msg.split()[1])
        return messages
