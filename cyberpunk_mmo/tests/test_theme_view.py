from django.test import TestCase
from django.urls import reverse


class ThemeViewTests(TestCase):
    def test_view_accepts_only_post(self):
        response = self.client.get(reverse("cyberpunk_mmo:set-theme"))
        self.assertEqual(response.status_code, 405)
