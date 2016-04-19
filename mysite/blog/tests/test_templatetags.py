# pylint: disable=missing-docstring

"""Custom template tags tests"""

from django.test import TestCase

from blog.factories import PostFactory
from blog.templatetags.blog_tags import total_posts


class TotalPostsTest(TestCase):

    def setUp(self):
        for _ in range(3):
            PostFactory()
            PostFactory(status='published')

    def test_returns_correct_result(self):
        self.assertEqual(total_posts(), 3)
