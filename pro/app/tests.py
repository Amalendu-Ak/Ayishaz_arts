
from django.test import TestCase

# Create your tests here.

class HomeViewTests(TestCase):
    def test_home_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

from django.test import TestCase

# Create your tests here.

