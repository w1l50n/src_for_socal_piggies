from celery import task, chain
from uuid import uuid4
from contextlib import closing
import subprocess
import logging

from twython import Twython
from djappsettings import settings
from rapidsms.router import send, lookup_connections


logger = logging.getLogger(__name__)


@task(max_retries=settings.TWITTER_MAX_RETRIES, default_retry_delay=settings.TWITTER_RETRY_DELAY)
def capture_image():
    try:
        file_path = "/tmp/{0}.jpg".format(uuid4().get_hex())
        cmd = "raspistill -w 1280 -h 720 -o {0}".format(file_path)
        return_code = subprocess.call(cmd.split())
        return file_path
    except Exception as ex:
        raise capture_image.retry(exc=ex)


@task(max_retries=settings.TWITTER_MAX_RETRIES, default_retry_delay=settings.TWITTER_RETRY_DELAY)
def send_twitter_status(file_path, status):
    try:
        twitter = Twython(settings.TWITTER_APP_KEY, settings.TWITTER_APP_SECRET,
                settings.TWITTER_OAUTH_TOKEN, settings.TWITTER_OAUTH_TOKEN_SECRET)

        with closing(open(file_path, 'rb')) as media:
            r = twitter.update_status_with_media(status=status, media=media)
            url = r.get('entities').get('media')[0].get('url')

        return url
    except Exception as ex:
        raise send_twitter_status.retry(exc=ex)

@task
def text_back(url, phone_number):
    try:
        connections = lookup_connections(backend="kannel-gsm-modem", identities=[phone_number])
        send(url, connections=connections)
    except Exception as ex:
        logger.warn(ex)
