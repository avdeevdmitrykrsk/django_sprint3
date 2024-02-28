from blog.models import Category, Post

from django.db.models import Q, QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils.timezone import now

POST_COUNT: int = 5


def index(request: HttpRequest) -> HttpResponse:
    """View-функция рендерит главную страницу с данными из БД."""
    template_name: str = 'blog/index.html'
    post_list: QuerySet = Post.objects.select_related(
        'author', 'category', 'location'
    ).filter(
        Q(pub_date__lte=now())
        & Q(is_published=True)
        & Q(category__is_published=True)
    ).order_by('-pub_date')[:POST_COUNT]
    context: dict = {
        'post_list': post_list
    }
    return render(request, template_name, context)


def post_detail(request: HttpRequest, post_id: int) -> HttpResponse:
    """View-функция рендерит страницу с описаниемконкретного товара."""
    template_name: str = 'blog/detail.html'
    post: object = get_object_or_404(
        Post.objects.select_related(
            'author', 'category', 'location'
        ).filter(pk=post_id),
        pub_date__lt=now(),
        is_published=True,
        category__is_published=True
    )
    context: dict = {
        'post': post
    }
    return render(request, template_name, context)


def category_posts(request: HttpRequest, category_slug: str) -> HttpResponse:
    """View-функция рендерит страницу с постами указаной категории."""
    template_name: str = 'blog/category.html'
    post_list: QuerySet = Post.objects.select_related(
        'author', 'category', 'location'
    ).filter(
        is_published=True,
        category__slug=category_slug,
        pub_date__lte=now()
    )
    category: object = get_object_or_404(
        Category.objects.values('title', 'description')
        .filter(is_published=True),
        slug=category_slug
    )
    context: dict = {
        'post_list': post_list,
        'category': category
    }
    return render(request, template_name, context)
