from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from .models import Campaign, Status, Teaser

def index(request):
    return HttpResponseRedirect(reverse('campaigns'))

class CampaignsView(LoginRequiredMixin, generic.ListView):
    model = Campaign
    template_name = 'advertiser/campaign_list.html'
    paginate_by = 10

    def get_queryset(self):
        return Campaign.objects.filter(user=self.request.user)

class CampaignDetailView(LoginRequiredMixin, generic.DetailView):
    model = Campaign

    def get_object(self, queryset=None):
        obj = super(CampaignDetailView, self).get_object()
        if not obj.user == self.request.user:
            raise Http404
        return obj

class CampaignCreate(LoginRequiredMixin, CreateView):
    model = Campaign
    fields = ['name', 'language', 'geo', 'browser', 'target_language', 'device', 'cpc', 'category', 'user_utm']
    success_url = reverse_lazy('campaigns')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CampaignCreate, self).form_valid(form)


class CampaignUpdate(LoginRequiredMixin, UpdateView):
    model = Campaign
    fields = ['name', 'category', 'geo', 'browser', 'target_language', 'device', 'cpc', 'user_utm']
    success_url = reverse_lazy('campaigns')
    template_name = 'advertiser/campaign_update.html'

    def get_object(self, queryset=None):
        obj = super(CampaignUpdate, self).get_object()
        if not obj.user == self.request.user:
            raise Http404
        return obj

class CampaignDelete(LoginRequiredMixin, DeleteView):
    model = Campaign
    success_url = reverse_lazy('campaigns')

    def get_object(self, queryset=None):
        obj = super(CampaignDelete, self).get_object()
        if not obj.user == self.request.user:
            raise Http404
        return obj

@login_required
def campaign_activate(request, pk):
    campaign_inst = get_object_or_404(Campaign, pk = pk)
    status = get_object_or_404(Status, pk=1)
    status_moderation = get_object_or_404(Status, pk=3)

    if campaign_inst.user == request.user and campaign_inst.status != status_moderation:
        campaign_inst.status = status
        campaign_inst.save()
        return HttpResponseRedirect(reverse('campaigns') )
    else:
        raise Http404

@login_required
def campaign_deactivate(request, pk):
    campaign_inst = get_object_or_404(Campaign, pk = pk)
    status = get_object_or_404(Status, pk = 2)
    status_moderation = get_object_or_404(Status, pk=3)

    if campaign_inst.user == request.user and campaign_inst.status != status_moderation:
        campaign_inst.status = status
        campaign_inst.save()
        return HttpResponseRedirect(reverse('campaigns') )
    else:
        raise Http404

class TeasersView(LoginRequiredMixin, generic.ListView):
    model = Teaser
    template_name = 'advertiser/teaser_list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        campaign = get_object_or_404(Campaign, pk=self.kwargs['campaign_id'], user=self.request.user)
        context = super(TeasersView, self).get_context_data(**kwargs)
        context['campaign'] = campaign
        return context

    def get_queryset(self):
        campaign = get_object_or_404(Campaign, pk=self.kwargs['campaign_id'], user=self.request.user)
        return Teaser.objects.filter(campaign=campaign)

class TeaserCreate(LoginRequiredMixin, CreateView):
    model = Teaser
    fields = ['title', 'image', 'url']
    template_name = 'advertiser/teaser_create.html'

    def form_valid(self, form):
        campaign = get_object_or_404(Campaign, pk=self.kwargs['campaign_id'], user=self.request.user)
        form.instance.campaign = campaign
        return super(TeaserCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse('teasers', kwargs={'campaign_id': self.kwargs['campaign_id']})

'''
    def form_valid(self, form):
        form.instance.campaign.user = self.request.user
        return super(TeaserCreate, self).form_valid(form)
'''

class TeaserDelete(LoginRequiredMixin, DeleteView):
    model = Teaser
    pk_url_kwarg = 'teaser_id'

    def get_success_url(self):
        return reverse('teasers', kwargs={'campaign_id': self.kwargs['campaign_id']})

    def get_object(self, queryset=None):
        obj = super(TeaserDelete, self).get_object()
        if not obj.campaign.user == self.request.user:
            raise Http404
        return obj

@login_required
def teaser_activate(request, campaign_id, teaser_id):
    teaser_inst = get_object_or_404(Teaser, pk = teaser_id)
    status = get_object_or_404(Status, pk=1)
    status_moderation = get_object_or_404(Status, pk=3)

    if teaser_inst.campaign.user == request.user and teaser_inst.status != status_moderation:
        teaser_inst.status = status
        teaser_inst.save()
        return HttpResponseRedirect(reverse('teasers', kwargs={'campaign_id': teaser_inst.campaign.pk}))
    else:
        raise Http404

@login_required
def teaser_deactivate(request, campaign_id, teaser_id):
    teaser_inst = get_object_or_404(Teaser, pk = teaser_id)
    status = get_object_or_404(Status, pk=2)
    status_moderation = get_object_or_404(Status, pk=3)

    if teaser_inst.campaign.user == request.user and teaser_inst.status != status_moderation:
        teaser_inst.status = status
        teaser_inst.save()
        return HttpResponseRedirect(reverse('teasers', kwargs={'campaign_id': teaser_inst.campaign.pk}))
    else:
        raise Http404