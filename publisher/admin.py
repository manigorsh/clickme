from django.contrib import admin
from .models import Site, Widget, Profile

admin.site.register(Profile)
admin.site.register(Site)
admin.site.register(Widget)