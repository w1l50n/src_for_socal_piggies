from pandas import DataFrame

from django.shortcuts import render_to_response
from django.template import RequestContext
from djappsettings import settings

from telesign_app.models import PhoneID


def phoneid(request):
    phoneids = PhoneID.objects.values('phone_number', 'carrier', 'phone_type',
                                        'lat', 'lon', 'iso2',
                                        'state', 'zip_code')

    columns  = ['phone_number', 'carrier', 'phone_type',
              'lat', 'lon', 'iso2',
              'state', 'zip_code']
    phoneids = PhoneID.objects.values(*columns)
    data_frame = DataFrame(list(phoneids))

    data = {
        'GOOGLE_API_KEY' : settings.GOOGLE_API_KEY,
        'phoneids' : phoneids,
        'phone_types' : data_frame['phone_type'].value_counts().to_dict(),
        'carriers' : data_frame['carrier'].value_counts().to_dict(),
        'lat_lon_list' : data_frame[['lat', 'lon']].dropna().values.tolist(),
        'pt' : data_frame['phone_type'].value_counts().to_dict(),
    }
    return render_to_response(
            "phoneid.html",
            data,
            context_instance=RequestContext(request))
