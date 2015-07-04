from django import forms
import datetime
from services.core_functions import monthdelta

from apps.payment.models import PaymentPlan, PaymentHistory
from apps.computer.models import Computer

DURATION_CHOICES = (
    ('--', '---- Select ----'),
    (6, '6 months'),
    (12, '12 months'),
    (18, '18 months'),
    (24, '24 months'),
)


class PaymentPlanForm(forms.Form):
    plan_duration = forms.TypedChoiceField(choices=DURATION_CHOICES, initial='--')

    def is_valid(self):
        if self.data['plan_duration'] != '--':
            return super(PaymentPlanForm, self).is_valid()


class PaymentHistoryForm(forms.Form):
    payment_start_date = forms.DateField(
        widget=forms.DateInput(attrs={'id': 'payment_start_date', 'type': 'date', 'value': datetime.date.today()}))
    amount_paid = forms.FloatField(widget=forms.NumberInput(
        attrs={'id': 'amount_paid', 'type': 'number', 'placeholder': 'Optional: For fellows with prior payments'}),
        required=False)
    payment_plan = forms.ModelChoiceField(queryset=PaymentPlan.objects.all(),
                                          widget=forms.Select(choices=(),
                                                              attrs={'id': 'payment_plan', 'required': 'True'}))
    computer = forms.ModelChoiceField(queryset=Computer.objects.all(),
                                      widget=forms.Select(choices=(), attrs={'id': 'computer', 'required': 'True'}))

    def save(self, fellow):
        data = self.data
        fellow.computer = Computer.objects.get(pk=data['computer'])
        payment_plan = PaymentPlan.objects.get(pk=data['payment_plan'])
        payment_history = PaymentHistory(fellow=fellow, previous_payment_plan=payment_plan,
                                         current_payment_plan=payment_plan)
        if data['amount_paid']:
            sum_paid = data['amount_paid']
            fellow.payment_start_date = data['payment_start_date']
            date = monthdelta(datetime.date.today(), -1)
            payment_history.date = date
            payment_history.sum_paid = sum_paid
        fellow.save()
        payment_history.save()
        return True
