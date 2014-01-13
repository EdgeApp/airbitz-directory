from django.conf.urls import patterns, include, url
from django.contrib import admin
from airbitz import settings

admin.autodiscover()

urlpatterns = patterns('',
    (r'^api/v1/', include('restapi.urls')),
    (r'^mgmt/', include('management.urls')),
    (r'^', include('directory.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^docs/', include('rest_framework_swagger.urls')),
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
           'document_root': settings.MEDIA_ROOT}))

