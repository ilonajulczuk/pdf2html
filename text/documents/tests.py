from django.test import TestCase
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
