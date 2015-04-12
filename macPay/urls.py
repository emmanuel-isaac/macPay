from django.conf.urls import patterns, include, url
from django.contrib import admin


from apps.macpayuser.views import (
    HomeView,
    LoginView,
    LogoutView,
    DashboardView,
)
from apps.payment.views import CreatePlanView

urlpatterns = patterns('',
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/', LoginView.as_view(), name='login'),
    url(r'^logout/', LogoutView.as_view(), name='logout'),
    url(r'^dashboard/', DashboardView.as_view(), name='dashboard'),
    url(r'^createplan/(?P<pk>\d+)/$', CreatePlanView.as_view(), name='create-plan'),
)
