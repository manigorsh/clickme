from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
]

urlpatterns += [
    url(r'^campaigns/$', views.CampaignsView.as_view(), name='campaigns'),
    url(r'^campaign/create/$', views.CampaignCreate.as_view(), name='campaign-create'),
    url(r'^campaign/(?P<pk>\d+)/update/$', views.CampaignUpdate.as_view(), name='campaign-update'),
    url(r'^campaign/(?P<pk>\d+)/delete/$', views.CampaignDelete.as_view(), name='campaign-delete'),
    url(r'^campaign/(?P<pk>[-\w]+)/activate/$', views.campaign_activate, name='campaign-activate'),
    url(r'^campaign/(?P<pk>[-\w]+)/deactivate/$', views.campaign_deactivate, name='campaign-deactivate'),
]

urlpatterns += [
    url(r'^campaign/(?P<campaign_id>\d+)/teasers/$', views.TeasersView.as_view(), name='teasers'),
    url(r'^campaign/(?P<campaign_id>\d+)/teaser/create/$', views.TeaserCreate.as_view(), name='teaser-create'),
    url(r'^campaign/(?P<campaign_id>\d+)/teaser/(?P<teaser_id>\d+)/delete/$', views.TeaserDelete.as_view(), name='teaser-delete'),
    url(r'^campaign/(?P<campaign_id>[-\w]+)/teaser/(?P<teaser_id>[-\w]+)/activate/$', views.teaser_activate, name='teaser-activate'),
    url(r'^campaign/(?P<campaign_id>[-\w]+)/teaser/(?P<teaser_id>[-\w]+)/deactivate/$', views.teaser_deactivate, name='teaser-deactivate'),
]