from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.http import HttpResponse
from django.views.generic import RedirectView
from airbitz import settings

admin.autodiscover()

import restapi.admin as a

mgmtapi = patterns('',
    url(r'^api/biz/$', a.AdminBusinessView.as_view()),
    url(r'^api/biz/(?P<pk>\d+)/?$', a.AdminBusinessDetails.as_view()),
    url(r'^api/biz/caplist/$', a.ScreencapList.as_view()),
    url(r'^api/biz/countries/$', a.RegionCountryQuery.as_view()),
    url(r'^api/biz/country/(?P<country>.*)/?$', a.RegionDetails.as_view()),
    url(r'^api/biz/published/$', a.PublishedDetails.as_view()),
    url(r'^api/biz/published/(?P<days>\d+)/?$', a.PublishedDetails.as_view()),

    url(r'^api/cat/$', a.AdminCategory.as_view()),
    url(r'^api/cat/(?P<pk>\d+)/?$', a.AdminCategoryDetail.as_view()),
)

urlpatterns = patterns('',
    (r'^api/v1/', include('restapi.urls')),
    (r'^mgmt/', include('management.urls')),
    (r'^mgmt/', include(mgmtapi, namespace='management')),
    url(r'^docs/', include('rest_framework_swagger.urls')),
    (r'^', include('directory.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^vote/$', 'management.views.redirect_vote', name='mgmt_redirect_vote'),
    url(r'^blog/$', 'management.views.redirect_blog', name='mgmt_redirect_blog'),
    url(r'^about/$', 'management.views.redirect_about', name='mgmt_redirect_about'),
    url(r'^privacy-policy/$', 'management.views.page_privacy_policy', name='page_privacy_policy'),
    url(r'^bitcoin-wallet/$', 'management.views.page_bitcoin_wallet', name='page_bitcoin_wallet'),
    url(r'^bitcoin-wallet-api-library/$', 'management.views.page_bitcoin_wallet_api_library', name='page_bitcoin_wallet_api_library'),
    url(r'^bitcoin-wallet-server-api/$', 'management.views.page_bitcoin_wallet_server_api', name='page_bitcoin_wallet_server_api'),
    url(r'^button/$', 'management.views.redirect_button', name='mgmt_redirect_button'),
    url(r'^rsvp/?$', RedirectView.as_view(url='http://www.meetup.com/Bitcoin-in-San-Diego/events/189727482/')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
           'document_root': settings.MEDIA_ROOT}))


# all urls except production servers should be blocked from search engines
if not settings.PRODUCTION:
    urlpatterns += patterns('',
        url(r'^robots\.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: /", mimetype="text/plain"))
    )
