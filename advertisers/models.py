from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Category(models.Model):
    class Meta:
        verbose_name_plural = "categories"
    name = models.CharField(max_length=200, help_text="Enter A Campaign's Category (e.g. WeightLoss, Health And Beauty and etc.)")

    def __str__(self):
        return self.name

class Language(models.Model):
    name = models.CharField(max_length=200,
                            help_text="Enter a the Campaign's Language (e.g. English, Spanish, Russian etc.)")

    def __str__(self):
        return self.name

class Status(models.Model):
    class Meta:
        verbose_name_plural = "statuses"
    name = models.CharField(max_length=200,
                            help_text="Enter a the Campaign's Status (e.g. Active, Paused and etc.)")

    def __str__(self):
        return self.name

class Geo(models.Model):
    name = models.CharField(max_length=200,
                            help_text="Enter a the Campaign's Geo (e.g. Russia, Spain and etc.)")

    def __str__(self):
            return self.name

class Browser(models.Model):
    name = models.CharField(max_length=200,
                            help_text="Enter a the Campaign's Browser (e.g. Google Chrome, Safari and etc.)")

    def __str__(self):
        return self.name

class Device(models.Model):
    name = models.CharField(max_length=200,
                            help_text="Enter a the Campaign's Device (e.g. Desktop, Mobile and etc.)")

    def __str__(self):
        return self.name

class Campaign(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, blank=False, null=False, default=3)
    language = models.ForeignKey(Language, on_delete=models.CASCADE, blank=False, null=False, default=1)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=False, null=False, default=1, help_text="Select A Category For This Campaign")
    geo = models.ManyToManyField(Geo, blank=True, help_text="Select A Geo For This Campaign (default all geos)")
    browser = models.ManyToManyField(Browser, blank=True, help_text="Select A Browser For This Campaign (default all browsers)")
    target_language = models.ManyToManyField(Language, blank=True, help_text="Select A Target Language For This Campaign (default all languages)", related_name='target_language')
    device = models.ManyToManyField(Device, blank=True, help_text="Select A Device For This Campaign (default all devices)")
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
    display_geo.short_description = 'Geo'

    def display_browser(self):
        return ', '.join([ browser.name for browser in self.browser.all() ])
    display_browser.short_description = 'Browser'

    def display_target_language(self):
        return ', '.join([ target_language.name for target_language in self.target_language.all() ])
        display_target_language.short_description = 'Language'

    def display_device(self):
        return ', '.join([ device.name for device in self.device.all() ])
    display_device.short_description = 'Device'

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