from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required, permission_required
import datetime


from apps.macpayuser.models import Fellow
from apps.payment.forms import PaymentPlanForm
from apps.computer.models import Computer
from apps.payment.models import PaymentHistory, PaymentPlan


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
            request.session['status'] = 'create'
            return HttpResponseRedirect(reverse('success'))

@login_required
def success(request):
    return render_to_response('success.html', locals())

class SyncPaymentView(View):
    def get(self, request):
        all_fellows = Fellow.objects.all()
        for fellow in all_fellows:
            try:
                last_payment_date = fellow.payment_histories.last().date.strftime('%m %y')
            except AttributeError, e:
                last_payment_date = ''
            current_date = datetime.datetime.now().strftime('%m %y')
            if last_payment_date != current_date and fellow.computer:
                payment_history = PaymentHistory(fellow=fellow, sum_paid=fellow.monthly_payment, payment_plan=fellow.recent_payment_plan)
                payment_history.save()
                print payment_history
            continue
        return HttpResponseRedirect(reverse('dashboard'))

class ChangePaymentPlanView(View):
    def get(self, request, pk):
        fellow = Fellow.objects.get(pk=pk)
        payment_plans = PaymentPlan.objects.all()
        form = PaymentPlanForm()
        return render_to_response('change-payment-plan.html', locals(), context_instance=RequestContext(request))

    def post(self, request, pk):
        form = PaymentPlanForm(request.POST)
        fellow = Fellow.objects.get(pk=pk)
        initial_payment_plan_duration = fellow.payment_plans.last().plan_duration
        if form.is_valid():
            payment_plan_change_val = request.POST.get('plan_duration', '')
            date_created = request.POST.get('date_created', '')
            if initial_payment_plan_duration != payment_plan_change_val:
                form.save()
                request.session['status'] = 'change'
                return HttpResponseRedirect(reverse('success'), locals())
            else:
                return HttpResponse('Not Done')


        









