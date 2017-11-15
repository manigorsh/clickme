from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from publisher.models import Widget
from advertiser.models import Status, Teaser, Language, Geo, Browser, Device, Campaign
from .models import Impression, Click, ClientInfo
import base64
from datetime import datetime

def getTeasers(request, widget_id, country_code, browser_name):
    ip = get_client_ip(request)

    language = Language.objects.filter(code=request.LANGUAGE_CODE[:2])
    geo = Geo.objects.filter(code=country_code)
    browser = Browser.objects.filter(name=browser_name)
    device = Device.objects.filter(pk=1)

    widget = get_object_or_404(Widget, pk=int(widget_id))
    status = get_object_or_404(Status, pk=1)

    teasers = Teaser.objects.filter(status=status, campaign__status=status, campaign__category=widget.category)
    if(language.count() == 0):
        teasers = teasers.filter(campaign__language = language)
    if(geo.count() == 0):
        teasers = teasers.filter(campaign__geo__in = geo)
    if (browser.count() != 0):
        teasers = teasers.filter(campaign__browser__in = browser)
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
        );

        impression.save()

        teaser.impressions += 1
        teaser.campaign.impressions += 1
        teaser.save();
        teaser.campaign.save();

        result["teasers"].append({
                "link" : 'http://127.0.0.1:8000/widget/click/' + unique_field +'/',
                "title" : teaser.title,
                "image" : teaser.image.url
                })

    return JsonResponse(result)

def click(request, click_id):
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

    impression = Impression.objects.filter(unique_field=click_id).first()
    import decimal
    impression.widget.earned += impression.click_price * decimal.Decimal(0.9);
    impression.widget.save()

    impression.widget.site.user.profile.balance += impression.click_price * decimal.Decimal(0.9);
    impression.widget.site.user.profile.save()

    impression.teaser.campaign.spent -= impression.click_price;
    impression.teaser.campaign.clicks += 1;
    impression.teaser.campaign.save();

    impression.teaser.campaign.user -= impression.click_price;
    impression.teaser.campaign.user.save();


    impression.teaser.clicks += 1;
    impression.teaser.save();

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

