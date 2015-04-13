from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required, permission_required


from apps.macpayuser.views import (
    HomeView,
    LoginView,
    LogoutView,
    DashboardView,
)
from apps.payment.views import CreatePlanView, success, SyncPaymentView, ChangePaymentPlanView

urlpatterns = patterns('',
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/', LoginView.as_view(), name='login'),
    url(r'^logout/', LogoutView.as_view(), name='logout'),
    url(r'^dashboard/', login_required( DashboardView.as_view() ), name='dashboard'),
    url(r'^createplan/(?P<pk>\d+)/$', login_required( CreatePlanView.as_view() ), name='create_plan'),
    url(r'^payment/success/$', success, name='success'),
    url(r'^sync-payment/$', login_required( SyncPaymentView.as_view() ), name='sync_payment'),
    url(r'^payment/change-plan/(?P<pk>\d+)/$', login_required( ChangePaymentPlanView.as_view() ), name='change_plan'),
)
