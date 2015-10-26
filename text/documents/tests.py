from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
import io

from documents.tasks import replace_links


class TestHtmlConversion(TestCase):
    def test_replacing_image_paths(self):
        text = '<img src="test.jpg">'
        want_text = '<img src="/media/test.jpg">'
        to_replace = [("test.jpg", "/media/test.jpg")]
        new_text = replace_links(text, to_replace)
        self.assertEquals(new_text, want_text)

    def test_stripping_to_body_content(self):
        # TODO(att): write proper test
        pass


class TestAPI(APITestCase):
    url = reverse('document-list')

    def setUp(self):
        self.user = User.objects.create_user(
            username='test', email='test@test.com', password='top_secret')

    def test_adding_document(self):
        self.client.login(username='test', password='top_secret')

        test_file = io.StringIO("test")
        test_file.name = "test.pdf"
        data = {"title": "test", "file": test_file}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieving_document(self):
        pass