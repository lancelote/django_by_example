# coding=utf-8
# pylint: disable=missing-docstring, no-member

"""Post detail page test"""

from selenium import webdriver
from pytz import UTC

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.utils import timezone

from blog.factories import PostFactory


class TestPostDetail(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.post = PostFactory(status='published', publish=timezone.datetime(2016, 10, 11, 2, 27, tzinfo=UTC))
        self.post.tags.add('tag0', 'tag1')

        # He create and tag few posts
        self.post1 = PostFactory(status='published')
        self.post2 = PostFactory(status='published')
        self.post3 = PostFactory(status='published')

        self.post1.tags.add('tag0', 'tag1')
        self.post2.tags.add('tag0')

        # User goes to the post page
        self.browser.get(self.live_server_url + self.post.get_absolute_url())

    def tearDown(self):
        self.browser.quit()

    def add_comment(self, name, email, body):
        self.browser.find_element_by_id('id_name').send_keys(name)
        self.browser.find_element_by_id('id_email').send_keys(email)
        self.browser.find_element_by_id('id_body').send_keys(body)
        self.browser.find_element_by_css_selector('input[type=submit]').click()

    def test_post_detail(self):
        # He sees the post title, date, author and body
        self.assertEqual(self.browser.find_element_by_css_selector('h1').text, self.post.title)
        self.assertEqual(self.browser.find_element_by_css_selector('#container p:nth-child(3)').text, self.post.body)
        date_author = 'Published Oct. 11, 2016, 5:27 a.m. by %s' % self.post.author.username
        self.assertEqual(self.browser.find_element_by_class_name('date').text, date_author)

    def test_comments(self):
        # He does not see any comments yet
        self.assertEqual(self.browser.find_element_by_id('comments-counter').text, '0 comments')
        self.assertEqual(self.browser.find_element_by_id('empty').text, 'There are no comments yet.')

        # But he see a form to enter a new comment
        self.browser.find_element_by_id('new-comment')

        # He adds a comment
        self.add_comment('user1', 'user1@example.com', 'First comment body')

        # And sees success message
        self.assertEqual(self.browser.find_element_by_id('adding-success').text, 'Your comment has been added.')

        # And his comment
        self.assertEqual(
            self.browser.find_element_by_css_selector('.comment p:last-child').text,
            'First comment body'
        )

        # He refreshes the page and adds two more comments
        self.browser.get(self.live_server_url + self.post.get_absolute_url())
        self.add_comment('user2', 'user2@example.com', 'Second comment body')
        self.browser.get(self.live_server_url + self.post.get_absolute_url())
        self.add_comment('user3', 'user3@example.com', 'Third comment body')

        # He sees all comments in right order
        comments = [comment.text for comment in self.browser.find_elements_by_css_selector('.comment p:last-child')]
        self.assertEqual(comments, ['First comment body', 'Second comment body', 'Third comment body'])

    def test_similar_posts(self):
        # He can see similar posts
        similar_posts = [post.text for post in self.browser.find_elements_by_css_selector('.similar-posts p a')]
        self.assertEqual(similar_posts, [self.post1.title, self.post2.title])

        # There is no similar posts for post3
        self.browser.get(self.live_server_url + self.post3.get_absolute_url())
        print(self.browser.find_element_by_class_name('similar-posts').text)
        self.assertEqual(
            self.browser.find_element_by_css_selector('.similar-posts p').text,
            'There are no similar posts yet.'
        )
