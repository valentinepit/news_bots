import logging

from defiyield import get_new_topics as defiyeld
from hacked import get_new_topics as hacked

logger = logging.getLogger(__name__)


def get_new_exploits():
    defiyeld_exploits = defiyeld()
    hacked_exploits = hacked()


get_new_exploits()
