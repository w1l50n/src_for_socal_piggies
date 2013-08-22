import re
import logging

from djappsettings import settings
from rapidsms.contrib.handlers import KeywordHandler, PatternHandler

from sms_raffle.models import RaffleEntry
from sms_raffle.tasks import choose_winners, rechoose_rpi, reset_winner


logger = logging.getLogger(__name__)


class RaffleHandler(KeywordHandler):
    keyword = "raffle"

    def help(self):
        self.handle("")

    def handle(self, text):
        try:
            obj, created = RaffleEntry.objects.get_or_create(phone_number=self.msg.phone_number)
            if created:
                self.respond("You are in! We will announce the winner at the end.")
            else:
                self.respond("Your already in the list :)")
        except Exception as ex:
            logger.warn(ex)        


class RaffleResultHandler(PatternHandler):
    pattern = r"^(\w+) winners"

    def handle(self, action):
        if self.msg.phone_number != settings.MY_PHONE_NUMER:
            return

        if action.lower() == "choose":
            choose_winners.delay()
        elif action.lower() == "rechoose_rpi":
            rechoose_rpi.delay()
        elif action.lower() == "reset_winner":
            reset.delay()
        else:
            action = "action unknow {0}".format(action)

        self.respond(action)
