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
        self.post2 = PostFactory()
        self.post3 = PostFactory(status='published')

    def tearDown(self):
        self.browser.quit()

    def test_post_list(self):
        # User goes to the main page
        self.browser.get(self.live_server_url + '/blog/')

        # He sees the list of published posts
        posts = self.browser.find_elements_by_css_selector('#container a')
        post_titles = [post.text for post in posts]
        self.assertIn(self.post1.title, post_titles)
        self.assertNotIn(self.post2.title, post_titles)
        self.assertIn(self.post3.title, post_titles)

        # He can go to specific post by click on it's title
        posts[0].click()
        self.assertEqual(self.browser.find_element_by_tag_name('h1').text, self.post3.title)
        self.assertEqual(self.browser.current_url, self.live_server_url + self.post3.get_absolute_url())
