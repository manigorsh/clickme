from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<widget_id>\d+)/teasers/$', views.getTeasers, name='get-teasers'),
    url(r'^click/(?P<click_id>)/$', views.click, name='get-teasers'),
]