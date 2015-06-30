from django.contrib import admin


from apps.macpayuser.models import StaffUser, Fellow, InviteStaff


# Register your models here.
admin.site.register(StaffUser)
admin.site.register(Fellow)
admin.site.register(InviteStaff)