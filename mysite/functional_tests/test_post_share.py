# pylint: disable=missing-docstring, no-member

"""Post share page test"""

from selenium import webdriver

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core import mail

from blog.factories import PostFactory


class TestPostShare(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.post = PostFactory(status='published')

    def tearDown(self):
        self.browser.quit()

    def test_post_share(self):
        # User can saw share link on a post detail page
        self.browser.get(self.live_server_url + self.post.get_absolute_url())
        share_url = self.browser.find_element_by_link_text('Share this post')

        # He click on it and redirects to share form
        share_url.click()
        self.assertEqual(self.browser.find_element_by_tag_name('h1').text, 'Share "%s" by e-mail' % self.post.title)

        # He clicks send button and sees required errors
        self.browser.find_element_by_id('send').click()
        self.assertEqual(len(self.browser.find_elements_by_class_name('errorlist')), 3)

        # He fills out the form and clicks send, than he sees a success page
        self.browser.find_element_by_id('id_name').send_keys('user')
        self.browser.find_element_by_id('id_sender').send_keys('user@example.com')
        self.browser.find_element_by_id('id_recipient').send_keys('to@example.com')
        self.browser.find_element_by_id('id_comments').send_keys('sample comment')
        self.browser.find_element_by_id('send').click()
        self.assertEqual(self.browser.find_element_by_tag_name('h1').text, 'E-mail successfully sent')

        # Email has been sent
        self.assertEqual(len(mail.outbox), 1)
        subject = 'user (user@example.com) recommends you reading "%s"' % self.post.title
        self.assertEqual(mail.outbox[0].subject, subject)
