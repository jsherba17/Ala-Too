from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views import View

from .models import Post, Tag
from .forms import PostForm, TagForm


def index(request):
    posts_list = Post.objects.all()
    return render(request, 'gallery/index.html', {'posts_list': posts_list})


def detail(request, pk):
    posts_list = Post.objects.all()
    try:
        post = Post.objects.get(pk=pk)
        total_likes = post.total_likes()
        total_views = post.total_views()
    except:
        raise Http404("Пост не найден.")
    try:
        post.views.add(request.user)
    except:
        return render(request, 'gallery/post.html',
                      {'post': post, 'posts_list': posts_list, 'total_likes': total_likes, 'total_views': total_views})

    return render(request, 'gallery/post.html',
                  {'post': post, 'posts_list': posts_list, 'total_likes': total_likes, 'total_views': total_views})


@login_required()
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('/', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'gallery/post_edit.html', {'form': form})


@login_required()
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('/', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'gallery/post_edit.html', {'form': form})


@login_required()
def post_delete(request, pk):
    post = Post.objects.get(pk=pk)
    post.delete()
    return redirect("/")


@login_required()
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.likes.add(request.user)
    return HttpResponseRedirect(reverse('gallery:detail', args=[str(pk)]))


def search(request):
    if request.method == 'GET':
        search_text = request.GET.get('search_input')
        try:
            status = Post.objects.filter(title__icontains=search_text)
            return render(request, 'gallery/search.html', {"search": status})
        except:
            return render(request, 'gallery/search.html', {})
    else:
        return render(request, "gallery/search.html", {})


def tags_list(request):
    tags = Tag.objects.all()
    return render(request, 'gallery/tags.html', {'tags': tags})


def tags_detail(request, title):
    tags = Tag.objects.get(title=title)
    return render(request, 'gallery/tags_detail.html', {'tags': tags})


class Tagcreate(View):
    def get(self, request):
        form = TagForm()
        return render(request, 'gallery/tag_create.html', {'form': form})

    def post(self, request):
        bound_form = TagForm(request.POST)
        if bound_form.is_valid():
            new_tag = bound_form.save()
            return redirect('/')
        return render(request, 'gallery/tag_create.html', {'form': bound_form})