"""Blog views"""
# pylint: disable=too-many-ancestors

from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from .models import Post


class PostListView(ListView):
    """List of published posts"""

    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_detail(request, year, month, day, post):
    """

    Args:
        request: HTTP Request
        year (str): '1972'
        month (str): '13'
        day (str): '20'
        post (str): post-slug
    """
    post = get_object_or_404(
        Post,
        slug=post,
        status='published',
        publish__year=year,
        publish__month=month,
        publish__day=day
    )
    return render(request, 'blog/post/detail.html', {'post': post})
