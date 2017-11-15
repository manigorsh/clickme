from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Category(models.Model):
    class Meta:
        verbose_name_plural = "categories"
    name = models.CharField(max_length=200, help_text="Choose a Category (e.g. WeightLoss, Health And Beauty and etc.)")

    def __str__(self):
        return self.name

class Language(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False, default="English", help_text="Choose a Language (e.g. English, Spanish, Russian etc.)")
    code = models.CharField(max_length=5, unique=True, null=False, blank=False, default="en", help_text="Choose a Language Code (e.g. en, es-ni, ru etc.)")

    def __str__(self):
        return "%s(%s)" % (self.name, self.code)

class Status(models.Model):
    class Meta:
        verbose_name_plural = "statuses"
    name = models.CharField(max_length=200, help_text="Choose a Status (e.g. Active, Paused and etc.)")

    def __str__(self):
        return self.name

class Geo(models.Model):
    name = models.CharField(max_length=44, null=True, help_text="Choose a Geo (e.g. Russia, Spain and etc.)")
    code = models.CharField(max_length=2, unique=True, null=True, help_text="Choose a Geo (e.g. ES, IT and etc.)")

    def __str__(self):
            return self.name

class Browser(models.Model):
    name = models.CharField(max_length=200, help_text="Choose a Browser (e.g. Google Chrome, Safari and etc.)")

    def __str__(self):
        return self.name

class Device(models.Model):
    name = models.CharField(max_length=200, help_text="Choose a Device (e.g. Desktop, Mobile and etc.)")

    def __str__(self):
        return self.name

class Campaign(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, blank=False, null=False, default=1)
    language = models.ForeignKey(Language, on_delete=models.CASCADE, blank=False, null=False, default=1, related_name='campaign_language')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=False, null=False, default=1, help_text="Select A Category For This Campaign")
    geo = models.ManyToManyField(Geo, default=1, blank=False, help_text="Select A Geo For This Campaign (default all geos)")
    browser = models.ManyToManyField(Browser, default=1, blank=False, help_text="Select A Browser For This Campaign (default all browsers)")
    device = models.ManyToManyField(Device, default=1, blank=False, help_text="Select A Device For This Campaign (default all devices)")
    user_utm = models.CharField(max_length=400, blank=True)
    impressions = models.BigIntegerField(default=0)
    clicks = models.BigIntegerField(default=0)
    spent = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    cpc = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('campaign-detail', args=[str(self.id)])

    def display_geo(self):
        return ', '.join([ geo.name for geo in self.geo.all() ])

    def display_browser(self):
        return ', '.join([ browser.name for browser in self.browser.all() ])

    def display_device(self):
        return ', '.join([ device.name for device in self.device.all() ])

    def display_num_teasers(self):
        return Teaser.objects.filter(campaign=self).count()


class Teaser(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to = 'teasers/') #414x232
    url = models.URLField(default='');
    campaign = models.ForeignKey(Campaign, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, blank=False, null=False, default=3)
    impressions = models.BigIntegerField(default=0)
    clicks = models.BigIntegerField(default=0)
    spent = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.title

    def get_ctr(self):
        if self.impressions != 0:
            return self.clicks / self.impressions
        else:
            return 'N/A'