"""Blog views"""

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404

from .models import Post


def post_list(request):
    """List of posts page /blog/

    Args:
        request: HTTP Request
    """
    object_list = Post.published.all()
    paginator = Paginator(object_list, 3)  # 3 posts per page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {
        'page': page,
        'posts': posts
    })


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
