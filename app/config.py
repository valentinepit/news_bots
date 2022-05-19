import logging

import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration

sentry_logging = LoggingIntegration(level=logging.INFO, event_level=logging.ERROR)

dsn = "https://cd6ebdfaf653491fadbac391ccf8d201@sentry.dexpa.io/26"

sentry_sdk.init(
    dsn=dsn,
    integrations=[sentry_logging],
    debug=False,
)


logging.basicConfig(format="%(asctime)s -%(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)
