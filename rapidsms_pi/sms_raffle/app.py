import re
import logging

from rapidsms.apps.base import AppBase


logger = logging.getLogger(__name__)
phone_number_re = re.compile(r"\D*(?P<phone_number>\d+)\D*")

class RaffleHandle(AppBase):

    def parse(self, msg):
        try:
            match = phone_number_re.match(msg.connection.identity)
            if match:
                msg.phone_number = match.groupdict().get('phone_number')
            else:
                msg.phone_number = msg.connection.identity.strip(" +")
        except Exception as ex:
            logger.warn(ex)
