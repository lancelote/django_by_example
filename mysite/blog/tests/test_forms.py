# pylint: disable=missing-docstring, invalid-name

"""Module docstring"""

from django.test import TestCase

from blog.forms import EmailPostForm


class EmailPostFormTest(TestCase):

    def test_form_validation_maximum_data(self):
        form = EmailPostForm(data={
            'name': 'user',
            'sender': 'example@test.com',
            'recipient': 'another@test.com',
            'comments': 'some comments'
        })
        self.assertTrue(form.is_valid())

    def test_form_validation_minimum_data(self):
        form = EmailPostForm(data={
            'name': 'user',
            'sender': 'example@test.com',
            'recipient': 'another@test.com'
        })
        self.assertTrue(form.is_valid())
