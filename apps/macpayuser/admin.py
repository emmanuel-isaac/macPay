from django.contrib import admin


from apps.macpayuser.models import StaffUser, Fellow, InviteStaff

@admin.register(Fellow)
class FellowAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'payment_start_date', 'computer']
    list_filter = ['payment_start_date', 'computer']

# Register your models here.
admin.site.register(StaffUser)
admin.site.register(InviteStaff)