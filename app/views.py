from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404

from app.models import Post


def index(request: HttpRequest) -> HttpResponse:
    qs = Post.objects.all()
    return render(request, "app/index.html", {"post_list": qs})


def post_detail(request: HttpRequest, pk: int) -> HttpResponse:
    # post = Post.objects.get(pk=pk)
    post = get_object_or_404(Post, pk=pk)  # get Objects를 했을 때 없으면 404
    return render(request, "app/post_detail.html", {"post": post})
