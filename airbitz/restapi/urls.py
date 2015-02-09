from django.conf.urls import patterns, url

import views as views
import restapi.admin as a

from notifications.views import NotificationView, HBitsPromoView, HBitsPromoMod

urlpatterns = patterns('',
     url(r'^business/(?P<bizId>\d+)/$', views.BusinessView.as_view()),
     url(r'^business/(?P<bizId>\d+)/photos/$', views.PhotosView.as_view()),

     url(r'^categories/$', views.CategoryView.as_view()),

     url(r'^category-suggest/?$', views.CategorySuggest.as_view()),
     url(r'^location-suggest/?$', views.LocationSuggest.as_view()),
     url(r'^autocomplete-business/?$', views.AutoCompleteBusiness.as_view()),
     url(r'^autocomplete-location/?$', views.AutoCompleteLocation.as_view()),

     url(r'^search/?$', views.SearchView.as_view()),

     url(r'^notifications/?$', NotificationView.as_view()),
     url(r'^hiddenbits/(?P<token>[a-zA-Z0-9]+)/?$', HBitsPromoView.as_view()),
     url(r'^promo/new/?$', HBitsPromoMod.as_view()),

     url(r'^business/submit/?$', a.ThirdPartyBusinessSubmit.as_view()),
     url(r'^business/list/?$', a.ThirdPartyBusinessList.as_view()),
     url(r'^business/list/(?P<provider_id>[a-zA-Z0-9]+)/?$', a.ThirdPartyBusinessList.as_view()),
     url(r'^categories/expense/?$', a.ThirdPartyExpenseCategoriesList.as_view()),
)

