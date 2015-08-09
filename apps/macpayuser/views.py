# Django Modules
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
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
from django.http import Http404


# Python Modules
import csv
import apps.macpayuser.templatetags.macpayuser_extras as dashboard_tags

# Create your views here.
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
            invite_id = request.session['invite_id']

            try:
                invite_staff = InviteStaff.objects.get(invite_id=invite_id)
                if timezone.now() < invite_staff.expiry_date:
                    invite_staff.user.is_active = True
                    invite_staff.user.save()

            except Exception as e:
                if e.message == 'InviteStaff matching query does not exist.':
                    raise Http404("Invalid invitation ID")

        return render_to_response('index.html', locals(), context_instance=RequestContext(request))

    def post(self, request):
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        if username and password:
            user = authenticate(username=username, password=password)

            if user and user.is_active:
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

        domain = get_current_site(request).domain

        for email in emails:
            msg = EmailMultiAlternatives(
                subject="Invitation to MacPay",
                from_email="MacPay <emmanuel.isaac@andela.co>",
                to=[email]
            )

            username = str(email.split('@')[0]).strip()

            ctx = {
                "username": username,
                "url_id": generate_invite_id(),
                "password": generate_password(),
                "user": request.user.username,
                "domain": domain
            }
            msg_invite = get_template('email.html').render(Context(ctx))
            msg.attach_alternative(msg_invite, "text/html")
            msg.send()

            user = User(username=ctx['username'], is_active=False)
            user.set_password(ctx['password'])
            user.save()

            invite = InviteStaff(user=user, invite_id=ctx['url_id'],
                                 date_created=datetime.datetime.now(),
                                 expiry_date=datetime.datetime.now() + timedelta(hours=48))
            invite.save()

        return render_to_response('invite-staff.html', context_instance=RequestContext(request))
