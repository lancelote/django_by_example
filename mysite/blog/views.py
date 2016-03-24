"""Blog views"""
# pylint: disable=too-many-ancestors

from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from .models import Post
from .forms import EmailPostForm, CommentForm


class PostListView(ListView):
    """List of published posts"""

    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_detail(request, year, month, day, post):
    """Show detail post page

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

    # Is there a new comment?
    new_comment = None

    # List of active comments of a given post
    comments = post.comments.filter(active=True)

    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request, 'blog/post/detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'new_comment': new_comment
    })


def post_share(request, post_id):
    """Post share view

    Args:
        request: HTTP Request
        post_id: Shared post id
    """
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        # From was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # From fields passed validation
            cleaned_data = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '%s (%s) recommends you reading "%s"' % (
                cleaned_data['name'], cleaned_data['sender'], post.title,)
            message = 'Read "%s" at %s\n\n%s\'s comments: %s' % (
                post.title, post_url, cleaned_data['sender'], cleaned_data['comments'])
            send_mail(subject, message, 'admin@myblog.com', [cleaned_data['recipient']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {
        'post': post,
        'form': form,
        'sent': sent
    })
