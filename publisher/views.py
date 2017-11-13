from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404

from .models import Site, Widget


def index(request):
    return HttpResponseRedirect(reverse('sites'))

class SitesView(LoginRequiredMixin, generic.ListView):
    model = Site
    template_name = 'publisher/site_list.html'
    paginate_by = 10

    def get_queryset(self):
        return Site.objects.filter(user=self.request.user)

class SiteCreate(LoginRequiredMixin, CreateView):
    model = Site
    template_name = 'publisher/site_create.html'
    fields = ['name', 'domain']
    success_url = reverse_lazy('sites')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(SiteCreate, self).form_valid(form)

class SiteDelete(LoginRequiredMixin, DeleteView):
    model = Site
    success_url = reverse_lazy('sites')

    def get_object(self, queryset=None):
        obj = super(SiteDelete, self).get_object()
        if not obj.user == self.request.user:
            raise Http404
        return obj

class WidgetsView(LoginRequiredMixin, generic.ListView):
    model = Widget
    template_name = 'publisher/widget_list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        site = get_object_or_404(Site, pk=self.kwargs['site_id'], user=self.request.user)
        context = super(WidgetsView, self).get_context_data(**kwargs)
        context['site'] = site
        return context

    def get_queryset(self):
        site = get_object_or_404(Site, pk=self.kwargs['site_id'], user=self.request.user)
        return Widget.objects.filter(site=site)

class WidgetCreate(LoginRequiredMixin, CreateView):
    model = Widget
    fields = ['title', 'category', 'geo', 'target_language']
    template_name = 'publisher/widget_create.html'

    def form_valid(self, form):
        site = get_object_or_404(Site, pk=self.kwargs['site_id'], user=self.request.user)
        form.instance.site = site
        return super(WidgetCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse('widgets', kwargs={'site_id': self.kwargs['site_id']})

class WidgetUpdate(LoginRequiredMixin, UpdateView):
    model = Widget
    fields = ['title', 'category', 'geo', 'target_language', 'rows', 'columns']
    template_name = 'publisher/widget_update.html'

    def get_object(self, queryset=None):
        obj = super(WidgetUpdate, self).get_object()
        if not obj.site.user == self.request.user:
            raise Http404
        return obj

    def get_success_url(self):
        return reverse('widgets', kwargs={'site_id': self.kwargs['site_id']})

class WidgetDelete(LoginRequiredMixin, DeleteView):
    model = Widget
    pk_url_kwarg = 'widget_id'

    def get_success_url(self):
        return reverse('widgets', kwargs={'site_id': self.kwargs['site_id']})

    def get_object(self, queryset=None):
        obj = super(WidgetDelete, self).get_object()
        if not obj.site.user == self.request.user:
            raise Http404
        return obj

