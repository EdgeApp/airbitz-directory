from django.conf.urls import patterns, url
from django.conf import settings

urlpatterns = patterns('',
    url(r'^coming_soon$', 'directory.views.coming_soon', name='coming_soon'),
    url(r'^search$', 'directory.views.business_search', name='search'),
    url(r'^biz/(?P<bizId>\d+)/$', 'directory.views.business_info', name='business_info'),
    url(r'^home/$', 'directory.views.home', name='home'),
    url(r'^$', 'directory.views.landing', name='landing'),
)


# Serve static_media files using the development server when not in production
# http://stackoverflow.com/questions/5517950/django-media-url-and-media-root
if settings.DEBUG:
    urlpatterns += patterns('',
       (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
           'document_root': settings.MEDIA_ROOT}))

    OTHER_STATIC=[
        "wp-content",
        "wp-includes",
        "assets",
    ]

    for i in OTHER_STATIC:
        urlpatterns += patterns('', (r'^(?P<path>' + i + '/.*)$',
            'django.views.static.serve',
            { 'document_root': settings.STATIC_ROOT}))