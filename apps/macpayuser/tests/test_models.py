from django.test import TestCase


from datetime import datetime
from dateutil.relativedelta import relativedelta


from apps.macpayuser.models import Fellow, StaffUser, DjangoUser
from apps.computer.models import Computer
from apps.payment.models import PaymentHistory, PaymentPlan


class StaffUserTestCase(TestCase):
    def setUp(self):
        user = DjangoUser.objects.create(first_name='Babajide', last_name='Bello')
        StaffUser.objects.create(user=user)

    def test_staffuser_fields(self):
        staff = StaffUser.objects.last()
        self.assertTrue(staff.user.is_staff, True)
        self.assertTrue(staff.user.is_superuser, True)
        self.assertTrue(staff.user.first_name, 'Babajide')


class FellowTestCase(TestCase):
    def setUp(self):
        self.computer = Computer.objects.create(name='MacBook', model='Pro 2014', cost=200000 )
        fellow = Fellow.objects.create(first_name='Ifedapo', last_name='Olarewaju', email='ifedapoolarewaju@andela.co', computer=self.computer )
        self.payment_plan = PaymentPlan.objects.create(plan_duration='12', fellow=fellow)
        self.payment_history = PaymentHistory.objects.create(fellow=fellow, sum_paid=40000.00, payment_plan=self.payment_plan)

    def test_fellow_fields(self):
        ifedapo = Fellow.objects.get(first_name='Ifedapo')
        self.assertEqual(ifedapo.last_name, 'Olarewaju')
        self.assertEqual(ifedapo.computer, self.computer)
        self.assertEqual(ifedapo.email, 'ifedapoolarewaju@andela.co')
        self.assertEqual(ifedapo.recent_payment_plan, self.payment_plan)
        self.assertEqual(ifedapo.amount_paid, 40000.00)
        self.assertEqual(ifedapo.due_balance, 160000.00)
        self.assertEqual(ifedapo.monthly_payment, 14545.45)
        
