from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin

from rapidsms.backends.kannel.views import KannelBackendView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    # RapidSMS core URLs
    (r'^accounts/', include('rapidsms.urls.login_logout')),
    url(r'^$', 'rapidsms.views.dashboard', name='rapidsms-dashboard'),
    # RapidSMS contrib app URLs
    (r'^httptester/', include('rapidsms.contrib.httptester.urls')),
    #(r'^locations/', include('rapidsms.contrib.locations.urls')),
    (r'^messagelog/', include('rapidsms.contrib.messagelog.urls')),
    (r'^messaging/', include('rapidsms.contrib.messaging.urls')),
    (r'^registration/', include('rapidsms.contrib.registration.urls')),

    # Third party URLs
    (r'^selectable/', include('selectable.urls')),

    # Kannel
    url(r"^backend/kannel-gsm-modem/$",
        KannelBackendView.as_view(backend_name="kannel-gsm-modem")),
    url(r'^kannel/', include('rapidsms.backends.kannel.urls')),

    # PhoneID
    url(r"^telesign/", include('telesign_app.urls')),

    # SMS Raffle
    url(r"^sms_raffle/", include('sms_raffle.urls')),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
