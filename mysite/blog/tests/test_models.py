# coding=utf-8

# pylint: disable=missing-docstring,no-member,invalid-name

"""
Models test
"""

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils.timezone import now

from blog.models import Post
from blog.factories import PostFactory, UserFactory


class TestPost(TestCase):

    def test_default_status_is_draft(self):
        self.assertEqual('draft', PostFactory().status)

    def test_can_not_create_two_posts_with_same_slug_and_date(self):
        publish = now()
        PostFactory(slug='sample_slug', publish=publish)
        self.assertRaises(ValidationError, Post(slug='sample_slug', publish=publish).validate_unique)

    def test_can_get_user_posts(self):
        user1 = UserFactory()
        user2 = UserFactory()
        post1 = PostFactory(title='first', author=user1)
        PostFactory(title='second', author=user2)
        post3 = PostFactory(title='third', author=user1)
        user1_posts = user1.blog_posts.all()

        self.assertEqual(len(user1_posts), 2)
        self.assertIn(post1, user1_posts)
        self.assertIn(post3, user1_posts)

    def test_post_order_is_reverse_publish(self):
        post1 = PostFactory(title='first')
        post2 = PostFactory(title='second')
        post3 = PostFactory(title='third')
        self.assertEqual(list(Post.objects.all()), [post3, post2, post1])
