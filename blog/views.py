from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from .models import Comment
from taggit.models import Tag


# Create your views here

# class PostListView(ListView):
#     # model = Post
#     queryset = Post.published.all()
#     context_object_name = 'posts'
#     paginate_by = 1
#     template_name = 'blog/post/list.html'


def post_list(requset, tag_slug=None):
    object_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])
    paginator = Paginator(object_list, 1)
    page = requset.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(requset, 'blog/post/list.html', {'page': page, 'posts': posts, 'tag':tag})


def post_detail(requset, year, month, day, post):
    post = get_object_or_404(Post, status='published', publish__year=year, publish__month=month, publish__day=day,
                             slug=post)
    comments = post.comments.filter(active=True)
    new_comment = None
    if requset.method == 'POST':
        comment_form = CommentForm(data=requset.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(requset, 'blog/post/detail.html', {'post': post, 'comments': comments,
                                                     'new_comment': new_comment, 'comment_form': comment_form})


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # send email:
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read:" \
                      f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                      f"{cd['name']}\'s comments : {cd['comments']}"
            send_mail(subject, message, 'mohammad.h.b.7798@gmail.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})
