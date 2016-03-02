# coding=utf-8
# pylint: disable=missing-docstring, no-member

"""Post list page test"""

from selenium import webdriver

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from blog.factories import PostFactory


class TestPostList(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.post1 = PostFactory(status='published')
        self.post2 = PostFactory(status='published')
        self.post3 = PostFactory()
        self.post4 = PostFactory(status='published')
        self.post5 = PostFactory(status='published')

    def tearDown(self):
        self.browser.quit()

    def can_see_actual_posts(self):
        posts = self.browser.find_elements_by_css_selector('#container a')
        post_titles = [post.text for post in posts]
        for post in [self.post5, self.post4, self.post2]:
            self.assertIn(post.title, post_titles)
        for post in [self.post3, self.post1]:
            self.assertNotIn(post.title, post_titles)

    def test_post_list(self):
        # User goes to the main page
        self.browser.get(self.live_server_url + '/blog/')

        # He sees the list of published posts
        self.can_see_actual_posts()

        # He can go to the second page and see old post
        self.browser.find_element_by_css_selector('.step-links a').click()
        self.assertEqual(self.browser.find_element_by_css_selector('#container a').text, self.post1.title)

        # And go back to the first page and see actual posts
        self.browser.find_element_by_css_selector('.step-links a').click()
        self.can_see_actual_posts()

        # He can go to specific post by click on it's title
        self.browser.find_element_by_css_selector('#container a').click()
        self.assertEqual(self.browser.find_element_by_tag_name('h1').text, self.post5.title)
        self.assertEqual(self.browser.current_url, self.live_server_url + self.post5.get_absolute_url())
