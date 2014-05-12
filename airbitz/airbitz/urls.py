from django.conf.urls import patterns, include, url
from django.contrib import admin
from airbitz import settings

admin.autodiscover()

import restapi.admin as a

mgmtapi = patterns('',
    url(r'^api/biz/$', a.AdminBusinessView.as_view()),
    url(r'^api/biz/(?P<pk>\d+)/?$', a.AdminBusinessDetails.as_view()),

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
    url(r'^factual/(?P<bizId>\d+)/$', 'management.views.factual_lookup', name='mgmt_factual_lookup'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
           'document_root': settings.MEDIA_ROOT}))

