# coding=utf-8
# pylint: disable=too-few-public-methods,missing-docstring

"""
Django Model Factories
"""

import factory

from django.contrib.auth.models import User

from blog import models


class UserFactory(factory.DjangoModelFactory):

    username = factory.Sequence(lambda n: 'test_user_%s' % n)
    first_name = 'John'
    last_name = 'Doe'
    email = factory.LazyAttribute(lambda x: '%s@example.org' % x.username)
    is_staff = False

    class Meta:
        model = User


class PostFactory(factory.DjangoModelFactory):

    title = factory.Sequence(lambda n: 'Sample Title %s' % n)
    slug = factory.Sequence(lambda n: 'sample-slug-%s' % n)
    author = factory.SubFactory(UserFactory)
    body = factory.Sequence(lambda n: 'Sample text %s' % n)

    class Meta:
        model = models.Post
