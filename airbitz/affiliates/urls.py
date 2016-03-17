from django.conf.urls import patterns, url

import views

urlpatterns = patterns('',
    url(r'^affiliates/register/?$', views.RegistrationView.as_view()),
    url(r'^affiliates/query/?$', views.QueryView.as_view(), name='affiliate_query'),
    url(r'^affiliates/(?P<token>.+)/?$', views.touch, name='affiliate_touch'),
    url(r'^af/(?P<token>.+)/?$', views.touch, name='affiliate_touch_short'),
)

