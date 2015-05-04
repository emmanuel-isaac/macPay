# Django Modules
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View
from django.contrib.auth import login, authenticate, logout
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.http import HttpResponse

# Python Modules
import csv


# Local Modules
from apps.macpayuser.models import Fellow
from services.skilltree import *



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
                print HttpResponseRedirect(reverse('home'))

        return HttpResponseRedirect(reverse('home'))

# Class Based Logout View
class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('home'), locals())


# Class Based Dashboard View
class DashboardView(View):
    def get(self, request):
        # Make API request to SkillTree to get the data of all fellows
        skilltree_instance = SkillTree()

        # instantiate params
        params = { 'page': 1 }
        data = []

        # The API request
        while SkillTree.get_data(skilltree_instance, params):
            response = SkillTree.get_data(skilltree_instance, params)
            data = data + response
            params['page'] += 1
            continue

        print data

        fellows = Fellow.objects.all()
        # Fellows with payment plans
        fellows_with_plan = []
        for fellow in fellows:
            if fellow.payment_plans.last():
                fellows_with_plan.append(fellow)
            continue
        return render_to_response('dashboard.html', locals(), context_instance=RequestContext(request))


def download_payment_data(request):
    # Get all fellows 
    fellows = Fellow.objects.all()

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="payment_data.csv"'

    writer = csv.writer(response)
    writer.writerow(['Fellow', 'Computer Model', 'Computer Cost', 'Payment Plan (months)', 'Monthly Payment', 'Payment Start Date', 'Amount Paid', 'Balance', 'Payment Plan Change Date', 'Final Payment Date'])

    for fellow in fellows:
        writer.writerow([fellow.first_name + ' ' + fellow.last_name, fellow.computer.name + ' ' + fellow.computer.model, fellow.computer.cost, fellow.recent_payment_plan.plan_duration, fellow.monthly_payment, fellow.payment_start_date, fellow.amount_paid, fellow.due_balance, fellow.last_plan_change_date, fellow.last_plan_change_date  ])
        continue

    return response


















