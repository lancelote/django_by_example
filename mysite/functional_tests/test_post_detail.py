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

    def tearDown(self):
        self.browser.quit()

    def test_post_detail(self):
        # User goes to the post page
        self.browser.get(self.live_server_url + self.post.get_absolute_url())

        # He sees the post title, date, author and body
        self.assertEqual(self.browser.find_element_by_css_selector('h1').text, self.post.title)
        self.assertEqual(self.browser.find_element_by_css_selector('#container p:nth-child(3)').text, self.post.body)
        date_author = 'Published Oct. 11, 2016, 5:27 a.m. by %s' % self.post.author.username
        self.assertEqual(self.browser.find_element_by_class_name('date').text, date_author)
