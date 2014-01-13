from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^login/$', 'management.views.login_user', name='mgmt_login'),
    url(r'^logout/$', 'management.views.logout_user', name='mgmt_logout'),

    url(r'^dashboard/$', 'management.views.dashboard', name='mgmt_dashboard'),
    url(r'^biz/import/$', 'management.views.business_import', name='mgmt_biz_import'),
    url(r'^biz/view/(?P<bizId>\d+)/main$', 'management.views.business_view', name='mgmt_biz_view'),
    url(r'^biz/add/$', 'management.views.business_base_edit', name='mgmt_biz_add'),
    url(r'^biz/edit/(?P<bizId>\d+)/main/$', 'management.views.business_base_edit', name='mgmt_biz_edit'),
    url(r'^biz/edit/(?P<bizId>\d+)/loc/$', 'management.views.business_location_edit', name='mgmt_biz_loc_edit'),
    url(r'^biz/edit/(?P<bizId>\d+)/hours/$', 'management.views.business_hours_edit', name='mgmt_biz_hours_edit'),
    url(r'^biz/edit/(?P<bizId>\d+)/social/$', 'management.views.business_social_edit', name='mgmt_biz_social_edit'),

    url(r'^biz/view/(?P<bizId>\d+)/images$', 'management.views.business_image_view', name='mgmt_biz_image_view'),
    url(r'^biz/view/(?P<bizId>\d+)/image/add$', 'management.views.business_image_edit', name='mgmt_biz_image_add'),
    url(r'^biz/view/(?P<bizId>\d+)/image/link$', 'management.views.business_image_link', name='mgmt_biz_image_link'),
    url(r'^biz/view/(?P<bizId>\d+)/images/edit/(?P<imgId>\d+)/$', 'management.views.business_image_edit', name='mgmt_biz_image_edit'),

    url(r'^biz/edit/(?P<bizId>\d+)/images/landing/(?P<imgId>\d+)/$', 'management.views.set_landing_image', name='mgmt_biz_set_landing_image'),
)

