# pylint: disable=invalid-name

"""Custom template tags for blog app"""

from django import template
from django.db.models import Count

from ..models import Post

register = template.Library()


@register.simple_tag
def total_posts():
    """Count number of published posts"""
    return Post.published.count()


@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    """Insert block of latest posts

    Args:
        count (int): Number of posts
    """
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


@register.assignment_tag
def get_most_commented_posts(count=5):
    """Return most commented posts

    Args:
        count (int): Number of posts
    """
    return Post.published.annotate(total_comments=Count('comments'))\
        .order_by('-total_comments')[:count]
