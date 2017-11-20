from django.db import models

class Lead(models.Model):
    email = models.EmailField(default='')
    domain = models.URLField(default='');