from django.conf.urls import patterns, url

import views as views

urlpatterns = patterns('',
     url(r'^business/(?P<bizId>\d+)/$', views.BusinessView.as_view()),
     url(r'^business/(?P<bizId>\d+)/photos/$', views.PhotosView.as_view()),

     url(r'^categories/$', views.CategoryView.as_view()),

     url(r'^location-suggest/?$', views.LocationSuggest.as_view()),
     url(r'^autocomplete-business/?$', views.AutoCompleteBusiness.as_view()),
     url(r'^autocomplete-location/?$', views.AutoCompleteLocation.as_view()),

     url(r'^search/?$', views.SearchView.as_view()),
)

