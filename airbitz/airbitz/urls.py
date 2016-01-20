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
    url(r'^team/$', 'management.views.redirect_team', name='mgmt_redirect_team'),
    url(r'^faq/$', 'management.views.redirect_faq', name='mgmt_redirect_faq'),
    url(r'^privacy-policy/$', 'management.views.page_privacy_policy', name='page_privacy_policy'),
    url(r'^card/$', 'management.views.page_card', name='page_card'),
    url(r'^hiddenbits/$', 'management.views.page_hiddenbits', name='page_hiddenbits'),
    url(r'^bitcoin-wallet/$', 'management.views.page_bitcoin_wallet', name='page_bitcoin_wallet'),
    url(r'^developer-api-library/$', 'management.views.page_developer_api_library', name='page_developer_api_library'),
    url(r'^sdk/$', 'management.views.page_developer_api_library', name='page_sdk'),
    url(r'^api-library/$', 'management.views.page_developer_api_library', name='page_api_library'),
    url(r'^client-server-architecture/$', 'management.views.page_client_server_architecture', name='page_client_server_architecture'),
    url(r'^core-white-paper/$', 'management.views.page_core_white_paper', name='page_core_white_paper'),
    url(r'^data-model/$', 'management.views.page_data_model', name='page_data_model'),
    url(r'^data-sync-architecture/$', 'management.views.page_data_sync_architecture', name='page_data_sync_architecture'),
    url(r'^server-api/$', 'management.views.page_server_api', name='page_server_api'),
    url(r'^button/$', 'management.views.redirect_button', name='mgmt_redirect_button'),
    url(r'^rsvp/?$', RedirectView.as_view(url='http://www.meetup.com/Bitcoin-in-San-Diego/events/189727482/')),
    url(r'^savemoney/?$', RedirectView.as_view(url='https://airbitz.co/go/savemoney/')),
    url(r'^survey/(?P<slug>[-\w]+)/?$', 'management.views.page_survey_slug', name='page_survey_slug'),
    url(r'^verification/', include('verification.urls')),
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
