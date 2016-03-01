"""Blog views"""

from django.shortcuts import render, get_object_or_404

from .models import Post


def post_list(request):
    """List of posts page /blog/

    Args:
        request: HTTP Request
    """
    posts = Post.published.all()
    return render(request, 'blog/post/list.html', {'posts': posts})


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
