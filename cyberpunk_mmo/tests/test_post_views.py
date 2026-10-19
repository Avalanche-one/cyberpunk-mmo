from django.test import TestCase
from django.urls import reverse

from cyberpunk_mmo.models import Post


class PostDetailViewTests(TestCase):
    def setUp(self):
        self.post = Post.objects.create(
            name="Test transmission",
            text="Test news content.",
        )

    def test_post_detail_displays_requested_post(self):
        response = self.client.get(
            reverse("cyberpunk_mmo:post-detail", args=[self.post.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "cyberpunk_mmo/post_detail.html")
        self.assertEqual(response.context["post"], self.post)
        self.assertContains(response, self.post.name)
        self.assertContains(response, self.post.text)

    def test_post_detail_returns_404_for_missing_post(self):
        response = self.client.get(
            reverse("cyberpunk_mmo:post-detail", args=[self.post.pk + 1])
        )

        self.assertEqual(response.status_code, 404)
