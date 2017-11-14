from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^click/(?P<click_id>.*)/$', views.click, name='set-click'),
    url(r'^(?P<widget_id>\d+)/teasers/$', views.getTeasers, name='get-teasers'),
]