from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from expenses.models import ExpenseIncome

class ExpenseTrackerTests(APITestCase):

    def setUp(self):
        # Create two regular users
        self.user1 = User.objects.create_user(username='user1', password='pass1234')
        self.user2 = User.objects.create_user(username='user2', password='pass1234')
        # Create a superuser
        self.superuser = User.objects.create_superuser(username='admin', password='adminpass')
        self.client = APIClient()

    def test_register_user(self):
        response = self.client.post('/api/auth/register/', {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpass123'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login_user(self):
        response = self.client.post('/api/auth/login/', {
            'username': 'user1',
            'password': 'pass1234'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def authenticate(self, username='user1', password='pass1234'):
        response = self.client.post('/api/auth/login/', {
            'username': username,
            'password': password
        }, format='json')
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")

    def test_auth_status_authenticated(self):
        self.authenticate('user1', 'pass1234')
        response = self.client.get('/api/auth/status/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'user1')
        self.assertEqual(response.data['is_authenticated'], True)

    def test_auth_status_unauthenticated(self):
        response = self.client.get('/api/auth/status/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_expense(self):
        self.authenticate()
        response = self.client.post('/api/expenses/', {
            'title': 'Test Expense',
            'description': 'Testing expense creation',
            'amount': '100.00',
            'transaction_type': 'debit',
            'tax': '10.00',
            'tax_type': 'flat'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(float(response.data['total']), 110.00)

    def test_tax_calculation_percentage(self):
        self.authenticate()
        response = self.client.post('/api/expenses/', {
            'title': 'Percent Tax',
            'description': '',
            'amount': '100.00',
            'transaction_type': 'debit',
            'tax': '10.00',
            'tax_type': 'percentage'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertAlmostEqual(float(response.data['total']), 110.00)

    def test_list_expenses_only_own(self):
        # Create expenses for both users
        ExpenseIncome.objects.create(
            user=self.user1, title='User1 Exp', amount=50,
            transaction_type='debit', tax=5, tax_type='flat'
        )
        ExpenseIncome.objects.create(
            user=self.user2, title='User2 Exp', amount=70,
            transaction_type='credit', tax=7, tax_type='flat'
        )

        self.authenticate('user1', 'pass1234')
        response = self.client.get('/api/expenses/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'User1 Exp')

    def test_superuser_can_see_all(self):
        ExpenseIncome.objects.create(
            user=self.user1, title='User1 Exp', amount=50,
            transaction_type='debit', tax=5, tax_type='flat'
        )
        ExpenseIncome.objects.create(
            user=self.user2, title='User2 Exp', amount=70,
            transaction_type='credit', tax=7, tax_type='flat'
        )

        self.authenticate('admin', 'adminpass')
        response = self.client.get('/api/expenses/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_permission_denied_on_other_users_record(self):
        exp = ExpenseIncome.objects.create(
            user=self.user2, title='User2 Exp', amount=50,
            transaction_type='debit', tax=5, tax_type='flat'
        )

        self.authenticate('user1', 'pass1234')
        response = self.client.get(f'/api/expenses/{exp.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
