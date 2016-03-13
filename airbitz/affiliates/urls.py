from django.conf.urls import patterns, url

import views

urlpatterns = patterns('',
    url(r'^register/?$', views.RegistrationView.as_view()),
    url(r'^query/?$', views.QueryView.as_view(), name='affiliate_query'),
    url(r'^(?P<token>.+)/?$', views.touch, name='affiliate_touch'),
)

