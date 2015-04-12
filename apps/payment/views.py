from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View
from django.core.urlresolvers import reverse
from django.template import RequestContext


from apps.macpayuser.models import Fellow
from apps.payment.forms import PaymentPlanForm
from apps.computer.models import Computer


# Create your views here.


class CreatePlanView(View):
    def get(self, request, pk):
        fellow = Fellow.objects.get(pk=pk)
        form = PaymentPlanForm()
        computers = Computer.objects.all()

        return render_to_response('create-plan.html', locals(), context_instance=RequestContext(request))

    def post(self, request, pk):
        print request.POST
        form = PaymentPlanForm(request.POST)
        if form.is_valid():
            form.save()
            mac_id = request.POST.get('mac', '')
            mac = Computer.objects.get(pk=mac_id)
            fellow = Fellow.objects.get(pk=pk)
            fellow.computer = mac
            fellow.save()
            print request.POST.get('mac', '')
            return HttpResponse('Done')