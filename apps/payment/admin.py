from django.contrib import admin

from apps.payment.models import PaymentPlan, PaymentHistory




class PaymentHistoryAdmin(admin.ModelAdmin):
    list_display = ['fellow', 'date', 'sum_paid']
    list_filter = ['date', 'fellow']

# Register your models here.





admin.site.register(PaymentPlan)
admin.site.register(PaymentHistory, PaymentHistoryAdmin)