from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from yatube.settings import PAGINATOR_PAGE
from .models import Post, Group, Comment, Follow, User
from .forms import PostForm, CommentForm


def index(request):
    post_list = Post.objects.all().order_by('-pub_date')
    paginator = Paginator(post_list, PAGINATOR_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'index.html',
        {'page': page}
    )


def group_posts(request, slug):
    """Представление страницы сообщества."""
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group)
    paginator = Paginator(posts, PAGINATOR_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'group.html', {
        'group': group,
        'page': page
    })


@login_required
def new_post(request):
    """view-функция на основе формы передает
    переменную в шаблон
    в случае POST-запроса мы передаем в переменную
    form полученные данные
    Далее мы проверяем эти данные на валидность"""
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('index')

    return render(request, 'new.html', {'form': form})


def profile(request, username):
    user = get_object_or_404(User, username=username)
    post_list = Post.objects.filter(author=user).order_by('-pub_date')
    paginator = Paginator(post_list, PAGINATOR_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'profile.html',
        {'author': user, 'page': page, 'paginator': paginator}
    )


@login_required
def post_edit(request, username, post_id):
    user = get_object_or_404(User, username=username)
    if request.user.username != username:
        return redirect('post', username, post_id)
    post = get_object_or_404(Post, pk=post_id)
    form = PostForm(request.POST or None,
                    files=request.FILES or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect('post', username, post_id)
    return render(request, 'new.html', {'user': user, 'form': form, 'post': post})


def page_not_found(request, exception):
    return render(
        request, 
        'misc/404.html', 
        {'path': request.path}, 
        status=404
    )


def server_error(request):
    return render(request, 'misc/500.html', status=500)


def post_view(request, username, post_id):
    form = CommentForm()
    user = get_object_or_404(User, username=username)
    posts = user.posts.all()
    post = get_object_or_404(Post, pk=post_id)
    comments = post.comments.all()
    return render(
        request,
        'post.html',
        {'author': user,
         'form': form,
         'posts': posts,
         'post': post,
         'comments': comments,
    })


@login_required
def add_comment(request, username, post_id):
    post = get_object_or_404(Post, author__username=username, id=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('post', username, post_id)


@login_required
def follow_index(request):
    posts = Post.objects.filter(author__follower__user=request.user)
    paginator = Paginator(posts, PAGINATOR_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'follow.html',
        {'page': page, 'paginator': paginator},
    )


@login_required
def profile_follow(request, username):
    user = User.objects.get(username=username)
    if request.user != user:
        Follow.objects.create(user=request.user, author=user)
        return redirect('profile', username=username)
    return redirect('follow_index')


@login_required
def profile_unfollow(request, username):
    author = User.objects.get(username=username)
    Follow.objects.filter(user=request.user, author=author).delete()
    return redirect('profile', username)