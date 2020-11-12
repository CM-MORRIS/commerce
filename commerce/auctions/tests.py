import unittest
from django.test import Client, TestCase
from .models import User, Listings


# Create your tests here.
class Tests(TestCase):

    def setUp(self):
        # Create User.
        user1 = User.objects.create(pk=1)

        # Create listings.
        listing = Listings.objects.create(user_id=user1, title="listing test", description="test description",
                                          IMG_URL="test url", category="music", starting_price=0.99,
                                          current_price=0.99)

    def test_index(self):
        c = Client()
        response = c.get("/")

        self.assertEqual(response.status_code, 200)

        # accesses passed in parameters to render html
        self.assertEqual(response.context["listings"].count(), 1)
