from django.contrib import admin

# Register your models here.

from .models import Category, Language, Status, Geo, Browser, Device, Campaign, Teaser

admin.site.register(Category)
admin.site.register(Language)
admin.site.register(Status)
admin.site.register(Geo)
admin.site.register(Browser)
admin.site.register(Device)
admin.site.register(Campaign)
admin.site.register(Teaser)