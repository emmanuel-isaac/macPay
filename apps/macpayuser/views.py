# Django Modules
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.views.generic import View
from django.contrib.auth import login, authenticate, logout
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.http import HttpResponse

# Python Modules
import csv

# Local Modules
from services.skilltree import *
import apps.macpayuser.templatetags.macpayuser_extras as dashboard_tags

# Create your views here.
# Class Based Home View
class HomeView(View):
    def get(self, request):
        return render_to_response('index.html', locals(), context_instance=RequestContext(request))


# Class Based Login View
class LoginView(View):
    def get(self, request):
        return HttpResponseRedirect(reverse('home'))

    def post(self, request):
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        if username and password:
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('dashboard'), locals())
            else:
                return HttpResponseRedirect(reverse('home'))

        return HttpResponseRedirect(reverse('home'))


# Class Based Logout View
class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('home'), locals())


# Class Based Dashboard View
class DashboardView(View):
    def get(self, request):
        fellows = Fellow.objects.all()
        # Fellows with MacBooks
        fellows_with_plan = filter(lambda x: x.paymenthistory_set.all(), fellows)
        return render_to_response('dashboard.html', locals(), context_instance=RequestContext(request))


def download_payment_data(request):
    # Get all fellows 
    fellows = Fellow.objects.all()

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="payment_data.csv"'

    writer = csv.writer(response)
    writer.writerow(
        ['Fellow', 'Computer Model', 'Computer Value', 'Payment Plan', 'Payment Start Date', 'Amount Paid', 'Balance',
         'Final Payment Date'])

    for fellow in fellows:
        if fellow.paymenthistory_set.all():
            writer.writerow(
                [fellow.first_name + ' ' + fellow.last_name, fellow.computer.name + ' ' + fellow.computer.model,
                 fellow.computer.cost, dashboard_tags.get_current_payment_plan(fellow), fellow.payment_start_date,
                 dashboard_tags.get_amount_paid(fellow), dashboard_tags.get_balance(fellow),
                 dashboard_tags.get_tentative_payment_end_date(fellow)])
            continue

    return response
