from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r"^phoneid/$", 'telesign_app.views.phoneid'),
)
