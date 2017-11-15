from django.db import models
from publisher.models import Widget
from advertiser.models import Teaser

class ClientInfo(models.Model):
    ip = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=512, blank=True)
    country_code = models.CharField(max_length=10, blank=True)

class Impression(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    teaser = models.ForeignKey(Teaser, on_delete=models.SET_NULL, null=True, blank=True)
    widget = models.ForeignKey(Widget, on_delete=models.SET_NULL, null=True, blank=True)
    click_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    unique_field = models.CharField(max_length=512, blank=True)
    client_info = models.ForeignKey(ClientInfo, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ["created"]

class Click(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    unique_field = models.CharField(max_length=512, blank=True)
    client_info = models.ForeignKey(ClientInfo, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ["created"]
