from django.shortcuts import render, render_to_response
from django.views.generic import View
from django.views.generic.list import ListView
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
#from django.contrib import messages

from apps.computer.models import Computer, ComputerImage
from apps.computer.forms import ComputerCreationForm

import cloudinary.uploader

import os
import datetime


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
            if request.FILES.get('photo-url', False):  
                photo = request.FILES['photo-url']
                photo_and_date = str(os.path.splitext(str(photo))[0] + '-' + str(datetime.datetime.now()))
                pub_id = photo_and_date.replace(" ", "")

                try:
                    comp_img_data = cloudinary.uploader.upload(photo, public_id=pub_id, allowed_formats = ['png, jpg, gif, bmp, psd, thm, tif'])
                    comp_img_details = ComputerImage(secure_url=comp_img_data['secure_url'], public_id=comp_img_data['public_id'], height=comp_img_data['height'], width=comp_img_data['width'], original_filename=comp_img_data['original_filename'])
                    comp_img_details.save()
                    comp_creation_form = form.save(commit=False)
                    comp_creation_form.comp_img = comp_img_details
                    comp_creation_form.save()
                    return HttpResponseRedirect(reverse('computer_list'))

                except Exception as e:
                    if e.message == 'Invalid image file':
                        # messages.error(request, 'Invalid image.')
                        request.session['action'] = 'create'
                        return render_to_response('computer_creation.html', locals(), context_instance = RequestContext(request))
            else:
                form.save()
                return HttpResponseRedirect(reverse('computer_list'))

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
            request.session['status'] = 'change'
            return HttpResponseRedirect(reverse('success'))

        else:
            return render_to_response('computer_creation.html', locals(), context_instance=RequestContext(request))


