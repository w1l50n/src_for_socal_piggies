import re
import logging

from djappsettings import settings
from rapidsms.apps.base import AppBase

from telesign_app.tasks import run_phoneid


logger = logging.getLogger(__name__)
phone_number_re = re.compile(r"\D*(?P<phone_number>\d+)\D*")


class PhoneNumberHandle(AppBase):

    def parse(self, msg):
        try:
            match = phone_number_re.match(msg.connection.identity)
            if match:
                msg.phone_number = match.groupdict().get('phone_number')
            else:
                msg.phone_number = msg.connection.identity.strip(" +")
        except Exception as ex:
            logger.warn(ex)


    def handle(self, msg):
        if settings.TS_RUN_PHONEID:
            try:
                run_phoneid.delay(msg.phone_number)
            except Exception as ex:
                logger.warn(ex)

        return False