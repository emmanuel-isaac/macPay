from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required, permission_required
import datetime

from apps.macpayuser.models import Fellow
from apps.payment.forms import PaymentPlanForm, PaymentHistoryForm
from apps.computer.models import Computer
from apps.payment.models import PaymentHistory, PaymentPlan
from apps.macpayuser.templatetags.macpayuser_extras import get_balance, get_months_left_on_plan

from services.core_functions import create_payment_history


# Create your views here.
class CreatePlanView(View):
    def get(self, request, pk):
        fellow = Fellow.objects.get(pk=pk)
        form = PaymentHistoryForm()
        return render_to_response('create-plan.html', locals(), context_instance=RequestContext(request))

    def post(self, request, pk):
        form = PaymentHistoryForm(request.POST)
        fellow = Fellow.objects.get(pk=pk)
        print form.is_valid()
        if form.is_valid():
            form.save(fellow)
            request.session['status'] = 'create'
            return HttpResponseRedirect(reverse('success'))

        return render_to_response('create-plan.html', locals(), context_instance=RequestContext(request))


@login_required
def success(request):
    return render_to_response('success.html', locals())


class SyncPaymentView(View):
    def get(self, request):
        fellows = Fellow.objects.all()
        fellows_last_payment = map(lambda x: x.paymenthistory_set.last(), fellows)
        fellows_balances = map(lambda x: get_balance(x), fellows)
        payments_per_fellow = map(lambda x: x.paymenthistory_set.all().count(), fellows)
        for i in xrange(0, len(fellows)):
            last_payment = fellows_last_payment[i]
            fellow = fellows[i]
            if fellows_last_payment[i]:
                # *------For Fellows with New Plans-------* #
                if payments_per_fellow[i] == 1 and not last_payment.sum_paid:
                    monthly_due = float(fellows[i].computer.cost) / last_payment.current_payment_plan.plan_duration
                    last_payment.sum_paid = monthly_due
                    fellow.payment_start_date = datetime.date.today()
                    fellow.save()
                    last_payment.save()
                # *------For Fellows that have not paid for current month-------* #
                elif last_payment.date.strftime('%m %y') != datetime.date.today().strftime('%m %y'):
                    monthly_due = float(fellows_balances[i]) / get_months_left_on_plan(fellow)
                    new_history = PaymentHistory(fellow=fellow, sum_paid=monthly_due,
                                                 current_payment_plan=last_payment.current_payment_plan,
                                                 previous_payment_plan=last_payment.current_payment_plan)
                    new_history.save()

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
        if form.is_valid():
            data = form.data
            last_payment = fellow.paymenthistory_set.last()
            last_payment.current_payment_plan = PaymentPlan.objects.get(plan_duration=data['plan_duration'])
            last_payment.save()
            return HttpResponseRedirect(reverse('success'), locals())
        else:
            return render_to_response('change-payment-plan.html', locals(), context_instance=RequestContext(request))
