from celery import task
import logging
from json import loads

from django.core.exceptions import ObjectDoesNotExist
from telesign.api import PhoneId
from djappsettings import settings

from telesign_app.models import PhoneID


logger = logging.getLogger(__name__)


@task
def run_phoneid(phone_number):

    data = None

    try:
        data = PhoneID.objects.get(phone_number=phone_number)
        if data:
            return loads(data.raw_json)
    except ObjectDoesNotExist:
        pass
    except Exception as ex:
        logger.warn(ex)

    try:
        phoneid = PhoneId(settings.TS_CUSTOMER_ID, settings.TS_SECRET_KEY)
        data = phoneid.standard(phone_number)
    except Exception as ex:
        logger.warn(ex)

    if data:
        try:
            params = {
                'reference_id' : data.data.get('reference_id'),
                'phone_number' : phone_number,
                'carrier' : data.data.get('carrier').get('name'),
                'phone_type' : data.data.get('phone_type').get('description'),
                'lat' : data.data.get('location').get('coordinates').get('latitude'),
                'lon' : data.data.get('location').get('coordinates').get('longitude'),
                'iso2' : data.data.get('location').get('country').get('iso2'),
                'state' : data.data.get('location').get('state'),
                'zip_code' : data.data.get('location').get('zip'),
                'raw_json' :data.raw_data,
            }   
            phoneid = PhoneID.objects.create(**params)
        except Exception as ex:
            logger.warn(ex)

        return data.data
