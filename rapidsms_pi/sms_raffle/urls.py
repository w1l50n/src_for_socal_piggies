from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r"^show_winners/$", 'sms_raffle.views.show_winners'),
    url(r"^choose_winners/$", 'sms_raffle.views.choose_winners'),
    url(r"^rechoose_rpi/$", 'sms_raffle.views.rechoose_rpi'),
    url(r"^reset_winner/$", 'sms_raffle.views.reset_winner'),
)
