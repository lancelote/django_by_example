# pylint: disable=missing-docstring, invalid-name

"""Custom template tags tests"""

from django.test import TestCase

from blog.factories import PostFactory, CommentFactory
from blog.templatetags.blog_tags import total_posts, show_latest_posts, get_most_commented_posts


class TotalPostsTest(TestCase):

    def setUp(self):
        for _ in range(3):
            PostFactory()
            PostFactory(status='published')

    def test_returns_correct_result(self):
        self.assertEqual(total_posts(), 3)


class ShowLatestPosts(TestCase):

    def setUp(self):
        self.posts = [PostFactory(status='published') for _ in range(10)]

    def test_returns_correct_result_with_default_argument(self):
        self.assertEqual(list(show_latest_posts()['latest_posts']), self.posts[::-1][:5])

    def test_returns_correct_result_with_non_default_argument(self):
        self.assertEqual(list(show_latest_posts(3)['latest_posts']), self.posts[::-1][:3])


class GetMostCommentedPostsTest(TestCase):

    def setUp(self):
        self.posts = []

        for i in range(5):
            post = PostFactory(status='published')
            self.posts.append(post)
            for _ in range(i):
                CommentFactory(post=post)

    def test_returns_correct_result_with_default_argument(self):
        self.assertEqual(list(get_most_commented_posts()), self.posts[::-1])

    def test_returns_correct_result_with_non_default_argument(self):
        self.assertEqual(list(get_most_commented_posts(3)), self.posts[::-1][:3])
