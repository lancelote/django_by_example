# pylint: disable=missing-docstring, invalid-name, no-member

"""Blog views tests"""

import unittest

from django.core import mail
from django.test import TestCase

from blog.factories import PostFactory
from blog.models import Comment


class PostListTest(TestCase):

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


class PostDetailTest(TestCase):

    def setUp(self):
        self.post = PostFactory(status='published')
        self.response = self.client.get(self.post.get_absolute_url())

    def test_post_detail_renders_detail_template(self):
        self.assertTemplateUsed(self.response, 'blog/post/detail.html')

    def test_response_contains_post_title(self):
        self.assertContains(self.response, self.post.title)

    def test_unknown_post_returns_404(self):
        response = self.client.get('/blog/2000/01/02/hello-world/')
        self.assertEqual(response.status_code, 404)

    def test_no_comments(self):
        self.assertEqual(self.response.context['post'], self.post)
        self.assertEqual(list(self.response.context['comments']), [])
        self.assertEqual(self.response.context['new_comment'], None)

    def test_incorrect_post(self):
        bad_response = self.client.post(self.post.get_absolute_url(), {})
        self.assertContains(bad_response, 'This field is required')
        self.assertEqual(self.response.context['new_comment'], None)

    def test_correct_post(self):
        good_response = self.client.post(self.post.get_absolute_url(), {
            'name': 'user',
            'email': 'user@example.com',
            'body': 'Sample comment body'
        })
        self.assertContains(good_response, 'Sample comment body')
        self.assertContains(good_response, 'Your comment has been added.')
        self.assertEqual(good_response.context['new_comment'], Comment.objects.get(post=self.post))


class PostShareTest(TestCase):

    def setUp(self):
        self.post = PostFactory(status='published')
        self.response = self.client.get('/blog/%s/share/' % self.post.id)

    def sample_post_share(self):
        return self.client.post('/blog/%s/share/' % self.post.id, data={
            'name': 'user',
            'sender': 'from@example.com',
            'recipient': 'to@example.com',
            'comments': 'sample comments'
        })

    def test_post_share_renders_share_template(self):
        self.assertTemplateUsed(self.response, 'blog/post/share.html')

    def test_response_contains_post_title(self):
        self.assertContains(self.response, self.post.title)

    def test_unknown_post_returns_404(self):
        response = self.client.get('/blog/999/share/')
        self.assertEqual(response.status_code, 404)

    def test_get_method_does_not_send_email(self):
        self.assertEqual(len(mail.outbox), 0)

    def test_get_method_returns_form(self):
        self.assertContains(self.response, 'form')

    def test_post_method_send_email(self):
        self.sample_post_share()
        subject = 'user (from@example.com) recommends you reading "%s"' % self.post.title
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, subject)

    def test_post_method_send_email_with_correct_url(self):
        self.sample_post_share()
        self.assertIn(self.post.get_absolute_url(), mail.outbox[0].body)

    def test_post_method_returns_success_message(self):
        post_response = self.sample_post_share()
        self.assertContains(post_response, '"%s" was successfully sent.' % self.post.title)

    def test_post_with_invalid_form_returns_form(self):
        bad_post_response = self.client.post('/blog/%s/share/' % self.post.id)
        self.assertContains(bad_post_response, 'form')
