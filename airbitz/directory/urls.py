from django.conf.urls import patterns, url, include
from django.conf import settings
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^app', 'directory.views.app_download', name='app_download'),
    url(r'^search$', 'directory.views.business_search', name='search'),
    url(r'^search/no-results/?$', 'directory.views.business_search_no_results', name='search_no_results'),
    # url(r'^search/area/(?P<arg_location>\w+)/$', 'directory.views.business_search', name='search_area'),
    # url(r'^search/term/(?P<arg_term>\w+)/$', 'directory.views.business_search', name='search_term'),
    # url(r'^search/cat/(?P<arg_category>\w+)/$', 'directory.views.business_search', name='search_category'),
    # url(r'^search/latlon/(?P<arg_ll>\w+)/$', 'directory.views.business_search', name='search_latlon'),
    url(r'^biz/(?P<bizId>\d+)/$', 'directory.views.business_info', name='business_info'),
    url(r'^biz/?P<slug>/$', 'directory.views.business_info', name='business_info'),
    url(r'^add-biz/?$', 'directory.views.add_business', name='business_add'),
    url(r'^home/$', 'directory.views.landing', name='home'),
    url(r'^blf/$', 'directory.views.redirect_blf', name='redirect_blf'),
    url(r'^btc-email-request/$', 'directory.views.btc_email_request', name='btc_email_request'),
    url(r'^btc-email-request/template-email-request.html/$', 'directory.views.email_request_template', name='email_request_template'),
    # url(r'^home2/$', 'directory.views.home_v2', name='home_v2'),
    # url(r'^test/$', 'directory.views.test', name='test'),
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
        urlpatterns += patterns('',
            (r'^(?P<path>' + i + '/.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
        )





###########################
# for angular partials to work they must be definied
# http://django-angular.readthedocs.org/en/latest/integration.html#partials
###########################
class PartialGroupView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super(PartialGroupView, self).get_context_data(**kwargs)
        # update the context
        return context


partial_patterns = patterns('',
    url(r'^placeLookup.html$', PartialGroupView.as_view(template_name='ng-partials/add-biz/placeLookup.html'), name='place_lookup'),
    url(r'^generalInfo.html$', PartialGroupView.as_view(template_name='ng-partials/add-biz/generalInfo.html'), name='general_info'),
    url(r'^locationInfo.html$', PartialGroupView.as_view(template_name='ng-partials/add-biz/locationInfo.html'), name='location_info'),
    url(r'^geoInfo.html$', PartialGroupView.as_view(template_name='ng-partials/add-biz/geoInfo.html'), name='geo_info'),
    url(r'^socialInfo.html$', PartialGroupView.as_view(template_name='ng-partials/add-biz/socialInfo.html'), name='social_info'),
    url(r'^bizHours.html$', PartialGroupView.as_view(template_name='ng-partials/add-biz/bizHours.html'), name='biz_hours'),
    url(r'^imageGather.html$', PartialGroupView.as_view(template_name='ng-partials/add-biz/imageGather.html'), name='image_gather'),
    url(r'^bizPreview.html$', PartialGroupView.as_view(template_name='ng-partials/add-biz/bizPreview.html'), name='biz_preview'),
    url(r'^finishedThankYou.html$', PartialGroupView.as_view(template_name='ng-partials/add-biz/finishedThankYou.html'), name='finished_thank_you'),
    url(r'^collectAllInfo.html$', PartialGroupView.as_view(template_name='ng-partials/add-biz/collectAllInfo.html'), name='collect_all_info'),
    url(r'^bizQuery.html$', PartialGroupView.as_view(template_name='ng-partials/add-biz/bizQuery.html'), name='biz_query'),
    url(r'^placeLookup.html$', PartialGroupView.as_view(template_name='ng-partials/placeLookup.html'), name='place_lookup'),
    url(r'^collectInfo.html$', PartialGroupView.as_view(template_name='ng-partials/collectInfo.html'), name='collection_info'),
    url(r'^bizHours.html$', PartialGroupView.as_view(template_name='ng-partials/bizHours.html'), name='biz_hours'),


    url(r'^region-list.html$', PartialGroupView.as_view(template_name='ng-partials/search-starter/region-list.html'), name='region_list'),
    url(r'^cat-list.html$', PartialGroupView.as_view(template_name='ng-partials/search-starter/cat-list.html'), name='cat_list'),
    url(r'^region.html$', PartialGroupView.as_view(template_name='ng-partials/search-starter/region.html'), name='region_show'),
)

urlpatterns += patterns('',
    url(r'^partials/', include(partial_patterns, namespace='partials')),
)





