from django.db import models
from advertiser.models import Category, Language, Status, Geo
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    epayments_wallet = models.CharField(max_length=20, help_text="Enter a Epayments Wallet Number (e.g. xxx-xxxxxx)")

class Site(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, blank=False, null=False, default=3)
    domain = models.URLField(default='');

    def __str__(self):
        return self.name

    def display_num_widgets(self):
        return Widget.objects.filter(site=self).count()


class Widget(models.Model):
    title = models.CharField(max_length=200)
    site = models.ForeignKey(Site, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=False, null=False, default=1, help_text="Select A Category For This Widget")
    geo = models.ManyToManyField(Geo, blank=True, help_text="Select A Geo For This Campaign (default all geos)")
    target_language = models.ManyToManyField(Language, blank=True, help_text="Select A Target Language For This Widget (default all languages)", related_name='widget_target_language')
    impressions = models.BigIntegerField(default=0)
    clicks = models.BigIntegerField(default=0)
    earned = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        ordering = ["impressions"]

    def __str__(self):
        return self.title

    def display_target_language(self):
        return ', '.join([ target_language.name for target_language in self.target_language.all() ])

    def display_geo(self):
        return ', '.join([ geo.name for geo in self.geo.all() ])

    def get_code(self):
        return "<style>*,::after,::before{box-sizing:border-box}.walla-container{width:100%%;padding-right:15px;padding-left:15px;margin-right:auto;margin-left:auto}@media (min-width:576px){.walla-container{max-width:540px}}@media (min-width:768px){.walla-container{max-width:720px}}@media (min-width:992px){.walla-container{max-width:960px}}@media (min-width:1200px){.walla-container{max-width:1140px}}.walla-row{display:-ms-flexbox;display:flex;-ms-flex-wrap:wrap;flex-wrap:wrap;margin-right:-15px;margin-left:-15px}.walla-col-lg-6,.walla-col-md-12,.walla-col-xl-4{position:relative;width:100%%;min-height:1px;padding-right:15px;padding-left:15px}@media (min-width:768px){.walla-col-md-12{-ms-flex:0 0 100%%;flex:0 0 100%%;max-width:100%%}}@media (min-width:992px){.walla-col-lg-6{-ms-flex:0 0 50%%;flex:0 0 50%%;max-width:50%%}}@media (min-width:1200px){.walla-col-xl-4{-ms-flex:0 0 33.333333%%;flex:0 0 33.333333%%;max-width:33.333333%%}}</style><div id=\"walla_widget_%d\"></div><script type=\"text/javascript\">var XHR=\"onload\"in new XMLHttpRequest?XMLHttpRequest:XDomainRequest,xhr=new XHR,teasers,teaserContainer;xhr.open(\"GET\",\"http://127.0.0.1:8000/widget/%d/teasers/\",!0),xhr.onload=function(){json=JSON.parse(this.responseText),teaserContainer=document.getElementById(\"walla_widget_%d\");var e=document.createElement(\"div\");e.className=\"walla-container\";var t=document.createElement(\"div\");t.className=\"walla-row\";for(var a=0;a<json.teasers.length;a++){var n=json.teasers[a],l=document.createElement(\"div\");l.className=\"walla-col-md-12 walla-col-lg-6 walla-col-xl-4\",l.innerHTML='<a href=\"\'+n.link+\'\" target=\"_blank\"><img alt=\\\''+n.title+'\\\' style=\"width: 100%%; display: block;\" src=\"\'+n.image+\'\"><p style=\"font-size:18px;line-height:1.25;\">\'+n.title+\"</p></a>\",t.appendChild(l)}var r=document.createElement(\"p\");r.innerHTML=json.title,e.appendChild(r),e.appendChild(t),teaserContainer.appendChild(e)},xhr.onerror=function(){console.log(\"Error loading teasers \"+this.status)},xhr.send();</script>"  % (self.pk, self.pk, self.pk)