from django.conf.urls import patterns, url
from django.conf import settings

urlpatterns = patterns('',
    url(r'^search$', 'directory.views.business_search', name='search'),
    url(r'^biz/(?P<bizId>\d+)/$', 'directory.views.business_info', name='business_info'),
    url(r'^add-biz/$', 'directory.views.add_business', name='business_add'),
    url(r'^home2/$', 'directory.views.home_v2', name='home_v2'),
    url(r'^home/$', 'directory.views.landing', name='home'),
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
