# Django Modules
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View
from django.contrib.auth import login, authenticate, logout
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.http import HttpResponse
from django.core.mail import send_mail, EmailMultiAlternatives, EmailMessage
from django.template import Context
from django.template.loader import render_to_string, get_template
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.models import User
from django.utils import timezone 


# Python Modules
import csv
import os, binascii
import datetime
from datetime import timedelta

# Local Modules
from apps.macpayuser.models import Fellow, InviteStaff
from services.skilltree import *

# Class Based Home View
class HomeView(View):

    def get(self, request):
        return render_to_response('index.html', locals(), context_instance=RequestContext(request))

# Class Based Login View
class LoginView(View):

    def get(self, request):
        if self.request.GET.dict():
            request.session['invite_id'] = self.request.GET.dict()['invite_id']
        return render_to_response('index.html', locals(), context_instance=RequestContext(request))

    def post(self, request):
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        get_invite_id = request.session['invite_id']

        if username and password:
            user = authenticate(username=username, password=password)
            if user and user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('dashboard'), locals())
            elif user and get_invite_id:
                user_details = InviteStaff.objects.get(invite_id=get_invite_id)
                if timezone.now() < user_details.expiry_date:
                    if user_details.username == username and user_details.check_password(password):
                        user_details.is_active = True
                        user_details.save()
                        login(request, user)
                        del request.session['invite_id']
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
        if fellow.payment_histories.all():
            writer.writerow([fellow.first_name + ' ' + fellow.last_name, fellow.computer.name + ' ' + fellow.computer.model, fellow.computer.cost, fellow.recent_payment_plan.plan_duration, fellow.monthly_payment, fellow.payment_start_date, fellow.amount_paid, fellow.due_balance, fellow.last_plan_change_date, fellow.last_plan_change_date  ])
            continue

    return response


def generate_invite_id():
    return binascii.b2a_hex(os.urandom(10))

def generate_password():
    return binascii.b2a_hex(os.urandom(3))

class InviteStaffView(View):
    def get(self, request):
        return render_to_response('invite-staff.html', context_instance=RequestContext(request))

    def post(self, request):
        emails = request.POST.get('staff-emails', False)
        if emails:
            emails = emails.split(',')
        else:
            print "No email entered"

        invite_staff = InviteStaff()
        
        domain = get_current_site(request).domain

        for email in emails:
            msg = EmailMultiAlternatives(
                subject="Invitation to MacPay",
                from_email="MacPay <emmanuel.isaac@andela.co>",
                to=[email]
            )

            ctx = { 
                    "email": email, 
                    "url_id": generate_invite_id(), 
                    "password": generate_password(),
                    "user": request.user.username,
                    "domain": domain
                  }
            msg_invite = get_template('email.html').render(Context(ctx))
            msg.attach_alternative(msg_invite, "text/html")
            msg.send()

            invite_staff.invite_id = ctx['url_id']
            invite_staff.username = ctx['email']
            invite_staff.set_password(ctx['password'])
            invite_staff.date_created = datetime.datetime.now()
            invite_staff.expiry_date =  datetime.datetime.now() + timedelta(hours=48)
            invite_staff.is_active = False
            invite_staff.save()
        
        return render_to_response('invite-staff.html', context_instance=RequestContext(request))

# class InviteStaffLoginView(View):
#     def get(self, request, pk):
#         request.sess
#         return render_to_response('index.html', context_instance=RequestContext(request))
