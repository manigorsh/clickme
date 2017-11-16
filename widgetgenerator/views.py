from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from publisher.models import Widget
from advertiser.models import Status, Teaser, Language, Geo, Browser, Device, Campaign
from .models import Impression, Click, ClientInfo
import base64
from datetime import datetime
from django.db.models import F
from django.db.models.functions import Cast
from django.db.models import FloatField

def getTeasers(request, widget_id, country_code, browser_name):
    ip = get_client_ip(request)

    language = Language.objects.filter(code=request.LANGUAGE_CODE[:2])
    geo = Geo.objects.filter(code=country_code)
    browser = Browser.objects.filter(name=browser_name)
    device = Device.objects.filter(pk=1)

    widget = get_object_or_404(Widget, pk=int(widget_id))
    status = get_object_or_404(Status, pk=1)

    teasers = Teaser.objects.filter(status=status, campaign__status=status, campaign__category=widget.category, campaign__geo__in = geo,
                                    campaign__language = language, campaign__browser__in = browser)\
        .annotate(ctr=Cast(F('clicks'),FloatField()) / Cast(F('impressions'),FloatField())).order_by('-ctr', '-campaign__cpc')

    if (device.count() != 0):
        teasers = teasers.filter(campaign__device__in = device)


    client_info = ClientInfo(
        ip = ip,
        user_agent = request.META['HTTP_USER_AGENT'],
        country_code = country_code
    )
    client_info.save()

    result = {}
    result["title"] = widget.title

    result["teasers"] = []
    for teaser in teasers:
        unique_field = encodeClicId(teaser.pk, widget.pk)
        impression = Impression(
            teaser = teaser,
            widget = widget,
            click_price = teaser.campaign.cpc,
            unique_field = unique_field,
            client_info = client_info
        )

        impression.save()

        teaser.impressions += 1
        teaser.campaign.impressions += 1
        teaser.save()
        teaser.campaign.save()

        result["teasers"].append({
                "link" : 'http://127.0.0.1:8000/widget/click/' + unique_field +'/',
                "title" : teaser.title,
                "image" : teaser.image.url
                })

    return JsonResponse(result)

def getJsCode(request, widget_id):
    return HttpResponse("""function getBrowser(){var e="";return window.chrome&&window.chrome.webstore?e="Chrome":"undefined"!=typeof InstallTrigger?e="Firefox":document.documentMode?e="IE":!document.documentMode&&window.StyleMedia?e="Edge":/constructor/i.test(window.HTMLElement)||function(e){return"[object SafariRemoteNotification]"===e.toString()}(!window.safari||safari.pushNotification)?e="Safari":(window.opr&&opr.addons||window.opera||navigator.userAgent.indexOf(" OPR/")>=0)&&(e="Opera"),e}function getTeasers(e){var t=new XHR;t.open("GET","http://127.0.0.1:8000/widget/1/teasers/"+e+"/"+getBrowser()+"/",!0),t.onload=function(){json=JSON.parse(this.responseText),teaserContainer=document.getElementById("walla_widget_1");var e=document.createElement("div");e.className="walla-container";var t=document.createElement("div");t.className="walla-row";for(var o=0;o<json.teasers.length;o++){var n=json.teasers[o],a=document.createElement("div");a.className="walla-col-md-12 walla-col-lg-6 walla-col-xl-4",a.innerHTML="<a target='_blank' href='"+n.link+"'><img style='width:100%;max-height:193px' alt='"+n.title+"' style='width: 100%; display: block;' src='"+n.image+"'><p style='font-size:18px;line-height:1.25;'>"+n.title+"</p></a>",t.appendChild(a)}var r=document.createElement("p");r.innerHTML=json.title,e.appendChild(r),e.appendChild(t),teaserContainer.appendChild(e)},t.onerror=function(){console.log("Error loading teasers "+this.status)},t.send()}var XHR="onload"in new XMLHttpRequest?XMLHttpRequest:XDomainRequest,country_code="00",geo=new XHR;geo.open("GET","http://ip-api.com/json",!0),geo.onload=function(){json=JSON.parse(this.responseText),country_code=json.countryCode,getTeasers(country_code)},geo.onerror=function(){getTeasers(country_code)},geo.send();""", content_type=':application/x-javascript')

def getCssCode(request, widget_id):
    return HttpResponse('*,::after,::before{box-sizing:border-box}.walla-container{width:100%;padding-right:15px;padding-left:15px;margin-right:auto;margin-left:auto}@media (min-width:576px){.walla-container{max-width:540px}}@media (min-width:768px){.walla-container{max-width:720px}}@media (min-width:992px){.walla-container{max-width:960px}}@media (min-width:1200px){.walla-container{max-width:1140px}}.walla-row{display:-ms-flexbox;display:flex;-ms-flex-wrap:wrap;flex-wrap:wrap;margin-right:-15px;margin-left:-15px}.walla-col-lg-6,.walla-col-md-12,.walla-col-xl-4{position:relative;width:100%;min-height:1px;padding-right:15px;padding-left:15px}@media (min-width:768px){.walla-col-md-12{-ms-flex:0 0 100%;flex:0 0 100%;max-width:100%}}@media (min-width:992px){.walla-col-lg-6{-ms-flex:0 0 50%;flex:0 0 50%;max-width:50%}}@media (min-width:1200px){.walla-col-xl-4{-ms-flex:0 0 33.333333%;flex:0 0 33.333333%;max-width:33.333333%}}', content_type='text/css')


def click(request, click_id):

    click = Click.objects.filter(unique_field=click_id).first()
    impression = Impression.objects.filter(unique_field=click_id).first()

    if not click:
        client_info = ClientInfo(
            ip = get_client_ip(request),
            user_agent = request.META['HTTP_USER_AGENT'],
            country_code = '',
        )
        client_info.save()

        click = Click(
            unique_field = click_id,
            client_info = client_info
        )
        click.save()

        import decimal
        impression.widget.earned += impression.click_price * decimal.Decimal(0.9)
        impression.widget.save()

        impression.widget.site.user.profile.balance += impression.click_price * decimal.Decimal(0.9)
        impression.widget.site.user.profile.save()

        impression.teaser.campaign.spent -= impression.click_price
        impression.teaser.campaign.clicks += 1
        impression.teaser.campaign.save()

        impression.teaser.campaign.user.profile.balance -= impression.click_price
        impression.teaser.campaign.user.save()


        impression.teaser.clicks += 1
        impression.teaser.save()

    return HttpResponseRedirect(impression.teaser.url)

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def encodeClicId(teaser_pk, widget_pk):
    return base64.b64encode(bytes(str(teaser_pk) + ',' + str(widget_pk) + ',' + str(datetime.now()), encoding='utf-8')).decode("utf-8")

def decodeClicId(click_id):
    return str(base64.b64decode(click_id.encode("utf-8")), 'utf-8').split(",")