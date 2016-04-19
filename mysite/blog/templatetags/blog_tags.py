# pylint: disable=invalid-name

"""Custom template tags for blog app"""

from django import template

from ..models import Post

register = template.Library()


@register.simple_tag
def total_posts():
    """Count number of published posts"""
    return Post.published.count()
