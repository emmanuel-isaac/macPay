from django.contrib import admin


from apps.macpayuser.models import StaffUser, Fellow


# Register your models here.
admin.site.register(StaffUser)
admin.site.register(Fellow)