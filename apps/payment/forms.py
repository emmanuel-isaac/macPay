from django.forms import ModelForm


from apps.payment.models import PaymentPlan





class PaymentPlanForm(ModelForm):

    class Meta:
        model = PaymentPlan
        fields = ['fellow', 'plan_duration', 'date_created']