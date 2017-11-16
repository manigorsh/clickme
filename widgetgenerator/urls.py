from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^click/(?P<click_id>.*)/$', views.click, name='set-click'),
    url(r'^(?P<widget_id>\d+)/teasers/(?P<country_code>\w{2})/(?P<browser_name>\w+)/$', views.getTeasers, name='get-teasers'),
    url(r'^(?P<widget_id>\d+)/js/$', views.getJsCode, name='get-widget-js'),
    url(r'^(?P<widget_id>\d+)/css/$', views.getCssCode, name='get-widget-css'),
]