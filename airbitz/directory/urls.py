from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^coming_soon$', 'directory.views.coming_soon', name='coming_soon'),
    url(r'^search$', 'directory.views.business_search', name='search'),
    url(r'^biz/(?P<bizId>\d+)/$', 'directory.views.business_info', name='business_info'),
    url(r'^$', 'directory.views.landing', name='landing'),
)

