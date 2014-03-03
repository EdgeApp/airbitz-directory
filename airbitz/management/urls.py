from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^login/$', 'management.views.login_user', name='mgmt_login'),
    url(r'^logout/$', 'management.views.logout_user', name='mgmt_logout'),

    url(r'^cat/list/$', 'management.views.category_list', name='mgmt_category_list'),
    url(r'^cat/add/$', 'management.views.category_edit', name='mgmt_category_add'),
    url(r'^cat/edit/(?P<catId>\d+)/main/$', 'management.views.category_edit', name='mgmt_category_edit'),
    url(r'^cat/delete/(?P<catId>\d+)/main/$', 'management.views.category_delete', name='mgmt_category_delete'),

    url(r'^tag/list/$', 'management.views.image_tag_list', name='mgmt_image_tag_list'),
    url(r'^tag/add/$', 'management.views.image_tag_edit', name='mgmt_image_tag_add'),
    url(r'^tag/edit/(?P<tagId>\d+)/$', 'management.views.image_tag_edit', name='mgmt_image_tag_edit'),
    url(r'^tag/delete/(?P<tagId>\d+)/$', 'management.views.image_tag_delete', name='mgmt_image_tag_delete'),

    url(r'^dashboard/$', 'management.views.dashboard', name='mgmt_dashboard'),
    url(r'^map/$', 'management.views.map', name='mgmt_map'),
    url(r'^biz/import/$', 'management.views.business_import', name='mgmt_biz_import'),
    url(r'^biz/view/(?P<bizId>\d+)/main$', 'management.views.business_view', name='mgmt_biz_view'),
    url(r'^biz/copy/(?P<bizId>\d+)/$', 'management.views.business_copy', name='mgmt_biz_copy'),
    url(r'^biz/add/$', 'management.views.business_base_edit', name='mgmt_biz_add'),
    url(r'^biz/edit/(?P<bizId>\d+)/main/$', 'management.views.business_base_edit', name='mgmt_biz_edit'),
    url(r'^biz/edit/(?P<bizId>\d+)/loc/$', 'management.views.business_location_edit', name='mgmt_biz_loc_edit'),
    url(r'^biz/edit/(?P<bizId>\d+)/hours/$', 'management.views.business_hours_edit', name='mgmt_biz_hours_edit'),
    url(r'^biz/edit/(?P<bizId>\d+)/social/$', 'management.views.business_social_edit', name='mgmt_biz_social_edit'),

    url(r'^biz/view/(?P<bizId>\d+)/images$', 'management.views.business_image_view', name='mgmt_biz_image_view'),
    url(r'^biz/view/(?P<bizId>\d+)/image/add$', 'management.views.business_image_edit', name='mgmt_biz_image_add'),
    url(r'^biz/view/(?P<bizId>\d+)/image/link$', 'management.views.business_image_link', name='mgmt_biz_image_link'),
    url(r'^biz/view/(?P<bizId>\d+)/images/edit/(?P<imgId>\d+)/$', 'management.views.business_image_edit', name='mgmt_biz_image_edit'),
    url(r'^biz/view/(?P<bizId>\d+)/images/delete/(?P<imgId>\d+)/$', 'management.views.image_delete', name='mgmt_image_delete'),

    url(r'^biz/edit/(?P<bizId>\d+)/images/landing/(?P<imgId>\d+)/$', 'management.views.set_landing_image', name='mgmt_biz_set_landing_image'),
)

