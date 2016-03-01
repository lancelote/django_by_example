# coding=utf-8
# pylint: disable=missing-docstring

"""Admin page tests"""

from selenium import webdriver

from django.contrib.auth import get_user_model
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from blog.factories import PostFactory


class TestPostAdmin(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.admin_user = get_user_model().objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='password'
        )
        PostFactory()
        PostFactory()

    def tearDown(self):
        self.browser.quit()

    def search_post_by_title(self, title):
        """Search for Posts with given text in title

        Args:
            title (str): Title text to search

        Returns:
            List of title elements
        """
        search_field = self.browser.find_element_by_id('searchbar')
        search_button = self.browser.find_element_by_css_selector('#changelist-search input[type="submit"]')

        search_field.clear()
        search_field.send_keys(title)
        search_button.click()

        return self.browser.find_elements_by_css_selector('.field-title a')

    def test_displayed_list(self):
        # Admin open admin panel
        self.browser.get(self.live_server_url + '/admin/')

        # He checks page title to be sure he is in the right place
        self.assertEqual(self.browser.title, 'Log in | Django site admin')

        # He enters his username and password and submits the form to log in
        login_form = self.browser.find_element_by_id('login-form')
        login_form.find_element_by_name('username').send_keys('admin')
        login_form.find_element_by_name('password').send_keys('password')
        login_form.find_element_by_css_selector('.submit-row input').click()

        # He sees link to Posts
        posts_link = self.browser.find_element_by_link_text('Posts')
        self.assertEqual(posts_link.get_attribute('href'), self.live_server_url + '/admin/blog/post/')

        # He clicks on Posts link and see table of posts with columns: title, slug, author, publish and status
        posts_link.click()
        self.assertEqual(self.browser.find_element_by_css_selector('.column-title a').text, 'TITLE')
        self.assertEqual(self.browser.find_element_by_css_selector('.column-slug a').text, 'SLUG')
        self.assertEqual(self.browser.find_element_by_css_selector('.column-author a').text, 'AUTHOR')
        self.assertEqual(self.browser.find_element_by_css_selector('.column-publish .text a').text, 'PUBLISH')
        self.assertEqual(self.browser.find_element_by_css_selector('.column-status .text a').text, 'STATUS')

        # He can filter by status, created date and publish date
        filter_div = self.browser.find_element_by_id('changelist-filter')
        filter_options = filter_div.find_elements_by_tag_name('h3')
        self.assertEqual(filter_options[0].text, 'By status')
        self.assertEqual(filter_options[1].text, 'By created')
        self.assertEqual(filter_options[2].text, 'By publish')

        # He can search by post title and body
        self.assertEqual(len(self.search_post_by_title('')), 2)

        posts = self.search_post_by_title('Sample Title 0')
        self.assertEqual(len(posts), 1)
        self.assertEqual(posts[0].text, 'Sample Title 0')

        posts = self.search_post_by_title('Sample Title 1')
        self.assertEqual(len(posts), 1)
        self.assertEqual(posts[0].text, 'Sample Title 1')

        posts = self.search_post_by_title('Sample Title 2')
        self.assertEqual(len(posts), 0)

        # He can see the date hierarchy links by publish date
        self.browser.find_element_by_class_name('xfull')

        # Posts sorted by status and than by publish date
        self.search_post_by_title('')
        self.assertEqual(self.browser.find_element_by_css_selector('th:last-child span').text, '1')
        self.assertEqual(self.browser.find_element_by_css_selector('th:nth-child(5) span').text, '2')

        # He start a new post
        self.browser.find_element_by_css_selector('.addlink').click()

        # He type in post title
        self.browser.find_element_by_id('id_title').send_keys('Hello World')

        # He sees that slug field auto-updates
        self.assertEqual(self.browser.find_element_by_id('id_slug').get_attribute('value'), 'hello-world')

        # He click at the author lookup button
        self.browser.find_element_by_id('lookup_id_author').click()
        self.browser.switch_to.window(self.browser.window_handles[1])

        # He choose author
        self.browser.find_element_by_css_selector('.row2 a').click()

        # he sees that author correctly selected
        self.browser.switch_to.window(self.browser.window_handles[0])
        self.assertEqual(self.browser.find_element_by_id('id_author').get_attribute('value'), '2')
