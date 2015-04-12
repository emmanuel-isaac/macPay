from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View
from django.core.urlresolvers import reverse
from django.template import RequestContext
import datetime


from apps.macpayuser.models import Fellow
from apps.payment.forms import PaymentPlanForm
from apps.computer.models import Computer
from apps.payment.models import PaymentHistory


# Create your views here.


class CreatePlanView(View):
    def get(self, request, pk):
        fellow = Fellow.objects.get(pk=pk)
        form = PaymentPlanForm()
        computers = Computer.objects.all()

        return render_to_response('create-plan.html', locals(), context_instance=RequestContext(request))

    def post(self, request, pk):
        form = PaymentPlanForm(request.POST)
        if form.is_valid():
            form.save()
            mac_id = request.POST.get('mac', '')
            mac = Computer.objects.get(pk=mac_id)
            fellow = Fellow.objects.get(pk=pk)
            fellow.computer = mac
            fellow.save()
            print request.POST.get('mac', '')
            return HttpResponseRedirect(reverse('create_plan_success'))

def create_plan_success(request):
    return render_to_response('create-plan-success.html', locals())

class SyncPaymentView(View):
    def get(self, request):
        all_fellows = Fellow.objects.all()
        for fellow in all_fellows:
            try:
                last_payment_date = fellow.payment_histories.last().date.strftime('%m %y')
            except AttributeError, e:
                last_payment_date = '0 0'
            current_date = datetime.datetime.now().strftime('%m %y')
            if last_payment_date != current_date:
                payment_history = PaymentHistory(fellow=fellow, sum_paid=fellow.monthly_payment, payment_plan=fellow.recent_payment_plan)
                payment_history.save()
                print payment_history
            continue
        return HttpResponseRedirect(reverse('dashboard'))
