from .models import Lead
from django.views.generic.edit import CreateView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse, reverse_lazy

def index(request):
    return HttpResponseRedirect(reverse('lead-create'))

class LeadCreate(CreateView):
    model = Lead
    template_name = 'landings/lead_create.html'
    fields = ['email', 'domain']
    success_url = reverse_lazy('sites')