from http import HTTPStatus

from django.test import TestCase, Client


class AboutURLTests(TestCase):
    @classmethod
    def setUp(self):
        self.guest_client = Client()

    def test_about_url_available_to_any_user(self):
        """Страницы author и tech доступны любым"""
        url_names = ['/about/author/', '/about/tech/']
        for url in url_names:
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)
