from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View
from django.contrib.auth import login, authenticate, logout
from django.core.urlresolvers import reverse
from django.template import RequestContext


from apps.macpayuser.models import Fellow

# Create your views here.



# Class Based Home View
class HomeView(View):

    def get(self, request):
        return render_to_response('index.html', locals())

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
        fellows = Fellow.objects.all()
        # Fellows with payment plans
        fellows_with_plan = []
        for fellow in fellows:
            if fellow.payment_plans.last():
                fellows_with_plan.append(fellow)
            continue
        return render_to_response('dashboard.html', locals(), context_instance=RequestContext(request))