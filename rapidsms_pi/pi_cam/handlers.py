from celery import chain
import logging

from rapidsms.contrib.handlers import KeywordHandler
from pi_cam.tasks import capture_image, send_twitter_status, text_back
from telesign_app.tasks import run_phoneid


logger = logging.getLogger(__name__)


class TweetHandler(KeywordHandler):
    keyword = "tweet"

    def help(self):
        self.handle("")

    def handle(self, text):
        try:
            chain(capture_image.s(),
                  send_twitter_status.s(text),
                  text_back.s(self.msg.connection.identity)).apply_async()
        except Exception as ex:
            logger.warn(ex)
            return
