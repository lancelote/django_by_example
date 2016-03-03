# coding=utf-8
# pylint: disable=missing-docstring, invalid-name, no-member

"""Blog views tests"""

import unittest

from django.test import TestCase

from blog.factories import PostFactory


class TestPostList(TestCase):

    def test_post_list_page_renders_list_template(self):
        response = self.client.get('/blog/')
        self.assertTemplateUsed(response, 'blog/post/list.html')

    def test_returns_correct_list_of_posts(self):
        post1 = PostFactory(status='published')
        post2 = PostFactory()
        post3 = PostFactory(status='published')
        response = self.client.get('/blog/')
        self.assertContains(response, post1.title)
        self.assertNotContains(response, post2.title)
        self.assertContains(response, post3.title)

    def test_returns_only_3_last_posts_by_default(self):
        posts = [PostFactory(status='published') for _ in range(4)]
        response = self.client.get('/blog/')
        self.assertNotContains(response, posts[0].title)
        for post in posts[1:]:
            self.assertContains(response, post.title)

    def test_second_page_returns_correct_posts(self):
        posts = [PostFactory(status='published') for _ in range(4)]
        response = self.client.get('/blog/?page=2')
        self.assertContains(response, posts[0].title)
        for post in posts[1:]:
            self.assertNotContains(response, post.title)

    @unittest.skip('Not for class based view')
    def test_returns_last_page_if_page_is_out_of_range(self):
        posts = [PostFactory(status='published') for _ in range(4)]
        response = self.client.get('/blog/?page=999')
        self.assertContains(response, posts[0].title)
        for post in posts[1:]:
            self.assertNotContains(response, post.title)


class TestPostDetail(TestCase):

    def setUp(self):
        self.post = PostFactory(status='published')
        self.response = self.client.get(self.post.get_absolute_url())

    def test_post_detail_renders_detail_template(self):
        self.assertTemplateUsed(self.response, 'blog/post/detail.html')

    def test_response_contains_post_title(self):
        self.assertContains(self.response, self.post.title)

    def test_unknown_post_returns_404(self):
        response = self.client.get('2000/01/02/hello-world/')
        self.assertEqual(response.status_code, 404)
