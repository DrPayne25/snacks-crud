from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Snack


class snackTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="tester", email="tester@email.com", password="pass"
        )

        self.snack = Snack.objects.create(
            title="Poptart", purchaser=self.user, description="worse than you think",
        )

    def test_string_representation(self):
        self.assertEqual(str(self.snack), "Poptart")
    
    def test_string_representation_not_working(self):
        self.assertNotEqual(str(self.snack), "Poptarts")

    def test_snack_content(self):
        self.assertEqual(f"{self.snack.title}", "Poptart")
        self.assertEqual(f"{self.snack.purchaser}", "tester")
        self.assertEqual(f"{self.snack.description}", "worse than you think")
    
    def test_snack_not_content(self):
        self.assertNotEqual(f"{self.snack.title}", "Poptarts")
        self.assertNotEqual(f"{self.snack.purchaser}", "testers")
        self.assertNotEqual(f"{self.snack.description}", "better than you think")

    def test_snack_list_view(self):
        response = self.client.get(reverse("snack_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Poptart")
        self.assertTemplateUsed(response, "snack-list.html")
    
    def test_snack_list_view_not_working(self):
        response = self.client.get(reverse("snack_list"))
        self.assertNotEqual(response.status_code, 300)
        self.assertNotContains(response, "Poptarts")
        self.assertTemplateNotUsed(response, "snack-lists.html")

    def test_snack_detail_view(self):
        response = self.client.get(reverse("snack_detail", args="1"))
        no_response = self.client.get("/100000/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "Purchaser: tester")
        self.assertTemplateUsed(response, "snack-detail.html")

    def test_snack_detail_view_not_working(self):
        response = self.client.get(reverse("snack_detail", args="1"))
        no_response = self.client.get("/100000/")
        self.assertNotEqual(response.status_code, 300)
        self.assertNotEqual(no_response.status_code, 304)
        self.assertNotContains(response, "Purchaser: testers")
        self.assertTemplateNotUsed(response, "snack-details.html")

    def test_snack_create_view(self):
        response = self.client.post(
            reverse("snack_create"),
            {
                "title": "Poptarts",
                "purchaser": self.user.id,
                "description": "worse than you think",
            }, follow=True
        )

        self.assertRedirects(response, reverse("snack_detail", args="2"))
        self.assertContains(response, "Details about - Poptarts")
