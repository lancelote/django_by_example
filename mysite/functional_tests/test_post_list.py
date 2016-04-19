# coding=utf-8
# pylint: disable=missing-docstring, no-member, attribute-defined-outside-init, invalid-name
# pylint: disable=too-many-instance-attributes

"""Post list page test"""

from selenium import webdriver

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from blog.factories import PostFactory


class TestPostList(StaticLiveServerTestCase):

    def setUp(self):
        self.post0 = PostFactory(status='published')
        self.post1 = PostFactory(status='published')
        self.post2 = PostFactory()
        self.post3 = PostFactory(status='published')
        self.post4 = PostFactory(status='published')

        self.post3.tags.add('test_tag_0')
        self.post4.tags.add('test_tag_0')
        self.post4.tags.add('test_tag_1')

        self.browser = webdriver.Firefox()
        self.browser.get(self.live_server_url + '/blog/')  # Go to the main page

    def tearDown(self):
        self.browser.quit()

    def can_see_actual_posts(self):
        posts = self.browser.find_elements_by_css_selector('#container a')
        post_titles = [post.text for post in posts]
        for post in [self.post4, self.post3, self.post1]:
            self.assertIn(post.title, post_titles)
        for post in [self.post2, self.post0]:
            self.assertNotIn(post.title, post_titles)

    def test_basic_post_list(self):
        # He sees the list of published posts
        self.can_see_actual_posts()

        # He can go to the second page and see old post
        self.browser.find_element_by_css_selector('.step-links a').click()
        self.assertEqual(self.browser.find_element_by_css_selector('#container a').text, self.post0.title)

        # And go back to the first page and see actual posts
        self.browser.find_element_by_css_selector('.step-links a').click()
        self.can_see_actual_posts()

        # He can go to specific post by click on it's title
        self.browser.find_element_by_css_selector('#container a').click()
        self.assertEqual(self.browser.find_element_by_tag_name('h1').text, self.post4.title)
        self.assertEqual(self.browser.current_url, self.live_server_url + self.post4.get_absolute_url())

    def test_post_list_tags(self):
        # He sees post4 has two tags
        posts = self.browser.find_elements_by_class_name('post')
        tags = posts[0].find_elements_by_css_selector('.tags a')
        self.assertListEqual([tag.text for tag in tags], ['test_tag_0', 'test_tag_1'])

        # And post3 has one tag
        tags = posts[1].find_elements_by_css_selector('.tags a')
        self.assertEqual([tag.text for tag in tags], ['test_tag_0'])

        # He clicks on the test_tag_0 and post list are filtered
        tags[0].click()
        self.assertEqual(self.browser.find_element_by_tag_name('h2').text, 'Posts tagged with "test_tag_0"')
        titles = [title.text for title in self.browser.find_elements_by_css_selector('.post h2 a')]
        self.assertListEqual(titles, [self.post4.title, self.post3.title])

    def test_blog_tags__total_posts(self):
        """Custom total_posts tag works fine"""
        # User sees number of published posts in the sidebar welcome message
        sidebar = self.browser.find_element_by_id('sidebar')
        welcome_message = sidebar.find_element_by_tag_name('p').text
        self.assertIn('4', welcome_message)

    def test_blog_tags__show_latest_posts(self):
        """Custom show_latest_posts tag works fine"""
        self.post5 = PostFactory(status='published')
        self.post6 = PostFactory(status='published')
        self.browser.get(self.live_server_url + '/blog/')

        # Users see five latest posts
        sidebar = self.browser.find_element_by_id('sidebar')
        expected_posts = [self.post6, self.post5, self.post4, self.post3, self.post1]
        posts = [post.text for post in sidebar.find_elements_by_css_selector('li a')]
        self.assertEqual(posts, [post.title for post in expected_posts])
