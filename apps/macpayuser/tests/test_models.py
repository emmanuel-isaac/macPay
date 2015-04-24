from django.test import TestCase


from apps.macpayuser.models import Fellow, StaffUser, DjangoUser
from apps.computer.models import Computer


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
        self.computer = Computer.objects.create(name='MacBook', model='Pro 2014', cost='2000' )
        Fellow.objects.create(first_name='Ifedapo', last_name='Olarewaju', email='ifedapoolarewaju@andela.co', computer=self.computer )

    def test_fellow_fields(self):
        ifedapo = Fellow.objects.get(first_name='Ifedapo')
        self.assertEqual(ifedapo.last_name, 'Olarewaju')
        self.assertEqual(ifedapo.computer, self.computer)
        self.assertEqual(ifedapo.email, 'ifedapoolarewaju@andela.co')
