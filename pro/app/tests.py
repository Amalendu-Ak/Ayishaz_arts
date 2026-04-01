<<<<<<< HEAD
from django.test import TestCase

# Create your tests here.

class HomeViewTests(TestCase):
    def test_home_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
=======
from django.test import TestCase

# Create your tests here.
>>>>>>> 855c29bce681cecb57ed5e27fb8e74abeff628d4
