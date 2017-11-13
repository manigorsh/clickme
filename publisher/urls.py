from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
]

urlpatterns += [
    url(r'^sites/$', views.SitesView.as_view(), name='sites'),
    url(r'^site/create/$', views.SiteCreate.as_view(), name='site-create'),
    url(r'^site/(?P<pk>\d+)/delete/$', views.SiteDelete.as_view(), name='site-delete'),
]

urlpatterns += [
    url(r'^site/(?P<site_id>\d+)/widgets/$', views.WidgetsView.as_view(), name='widgets'),
    url(r'^site/(?P<site_id>\d+)/widgets/create/$', views.WidgetCreate.as_view(), name='widget-create'),
    url(r'^site/(?P<site_id>\d+)/widgets/(?P<widget_id>\d+)/update/$', views.WidgetUpdate.as_view(), name='widget-update'),
    url(r'^site/(?P<site_id>\d+)/widgets/(?P<widget_id>\d+)/delete/$', views.WidgetDelete.as_view(), name='widget-delete'),
]