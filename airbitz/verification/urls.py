from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^verify/(?P<verify_id>[\w]+)$', views.verify, name='verify'),
    url(r'^new/$', views.new, name='new'),
]