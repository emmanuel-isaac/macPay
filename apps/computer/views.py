from django.shortcuts import render, render_to_response
from django.views.generic import View
from django.views.generic.list import ListView
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse


from apps.computer.models import Computer
from apps.computer.forms import ComputerCreationForm




# Create your views here.

class ComputerListView(ListView):

    model = Computer

    def get_context_data(self, **kwargs):
        context = super(ComputerListView, self).get_context_data(**kwargs)
        context['request'] = self.request
        return context



class CreateComputerView(View):
    def get(self, request):
        form = ComputerCreationForm()
        request.session['action'] = 'create'
        return render_to_response('computer_creation.html', locals(), context_instance = RequestContext(request))

    def post(self, request):
        form = ComputerCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('success'))

        return render_to_response('computer_creation.html', locals(), context_instance=RequestContext(request))


class EditComputerView(View):
    def get(self, request, pk):
        computer = Computer.objects.get(pk=pk)
        form = ComputerCreationForm()
        request.session['action'] = 'edit'
        return render_to_response('computer_creation.html', locals(), context_instance=RequestContext(request))

    def post(self, request, pk):
        form = ComputerCreationForm(request.POST)
        computer = Computer.objects.get(pk=pk)
        if form.is_valid():
            computer.name = request.POST.get('name')
            computer.model = request.POST.get('model')
            computer.cost = request.POST.get('cost')
            computer.save()
            return HttpResponseRedirect(reverse('success'))

        else:
            return render_to_response('computer_creation.html', locals(), context_instance=RequestContext(request))


