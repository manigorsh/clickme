from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from publisher.models import Widget
from advertiser.models import Status, Teaser
from .models import Impression, Click, ClientInfo
import base64
from datetime import datetime

def getTeasers(request, widget_id):
    widget = get_object_or_404(Widget, pk=int(widget_id))
    status = get_object_or_404(Status, pk=1)
    #teasers = Teaser.objects.filter(category=widget.category, status=status, campaign__target_language=widget.target_language)
    #teasers = Teaser.objects.filter(status=status)
    teasers = Teaser.objects.filter()

    client_info = ClientInfo(
        ip = get_client_ip(request),
        user_agent = '',
        country = '',
        city = '',
    );
    client_info.save()

    result = {}
    result["title"] = widget.title

    result["teasers"] = []
    for teaser in teasers:
        unique_field = str(teaser.pk) + str(widget.pk) + ',' + str(widget.pk) + ',' + str(widget.pk) + ',' + str(datetime.now())
        unique_field_b = bytes(unique_field, encoding='utf-8')
        unique_field_base64 = base64.b64encode(unique_field_b)
        unique_field_base64_d = unique_field_base64.decode("utf-8")
        impression = Impression(
            teaser = teaser,
            widget = widget,
            click_price = teaser.campaign.cpc,
            unique_field = unique_field_base64_d,
            client_info = client_info,
        );

        impression.save()

        result["teasers"].append({
                "link" : 'http://127.0.0.1:8000/widget/click/' + unique_field_base64_d +'/',
                "title" : teaser.title,
                "image" : teaser.image.url
                })

    return JsonResponse(result)

def click(request, click_id):
    pass

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip