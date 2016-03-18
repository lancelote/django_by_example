# coding=utf-8

# pylint: disable=missing-docstring,no-member,invalid-name

"""Blog models test"""

from pytz import UTC

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from blog.models import Post, Comment
from blog.factories import PostFactory, UserFactory, CommentFactory


class TestPost(TestCase):

    def test_default_status_is_draft(self):
        self.assertEqual('draft', PostFactory().status)

    def test_can_not_create_two_posts_with_same_slug_and_date(self):
        publish = timezone.now()
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

    def test_absolute_url(self):
        post1 = PostFactory(slug='sample-slug-0', publish=timezone.datetime(2016, 10, 11, tzinfo=UTC))
        self.assertEqual(post1.get_absolute_url(), '/blog/2016/10/11/sample-slug-0/')


class TestPublishedManager(TestCase):

    def test_published_manager_returns_only_published_posts(self):
        post1 = PostFactory(status='published')
        PostFactory()
        post3 = PostFactory(status='published')
        self.assertListEqual(list(Post.published.all()), [post3, post1])


class TestComments(TestCase):

    def test_comments_are_ordered_by_created_time(self):
        comment1 = CommentFactory()
        comment2 = CommentFactory()
        comment3 = CommentFactory()
        self.assertEqual(list(Comment.objects.all()), [comment1, comment2, comment3])

    def test_can_get_all_post_comments(self):
        post = PostFactory()
        comment1 = CommentFactory(post=post)
        CommentFactory()  # Comment from another post
        comment3 = CommentFactory(post=post)
        self.assertEqual(list(post.comments.all()), [comment1, comment3])

    def test_comment_str_representation(self):
        post = PostFactory(title='test-post')
        comment = CommentFactory(name='test-user', post=post)
        self.assertEqual(comment.__str__(), 'Comment by test-user on test-post')
