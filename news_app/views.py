from django.shortcuts import render, get_object_or_404
from .models import Post, Category, Adv
from django.db.models import Q
import random


def get_random_advs(count=4):
    """Вернуть случайные рекламы"""
    all_advs = list(Adv.objects.all())
    if len(all_advs) <= count:
        return all_advs
    return random.sample(all_advs, count)


def home_page(request):
    hot_posts = Post.objects.all().order_by('-created_at')[:4]
    # Рандомные посты (не из hot_posts)
    hot_ids = list(hot_posts.values_list('id', flat=True))
    other_posts = list(Post.objects.exclude(id__in=hot_ids))
    random_posts = random.sample(other_posts, min(6, len(other_posts)))
    advs = get_random_advs(4)
    context = {
        'hot_posts': hot_posts,
        'posts': random_posts,
        'advs': advs,
    }
    return render(request, "index.html", context)


def all_news_page(request):
    posts = Post.objects.all().order_by('-created_at')
    advs = get_random_advs(4)
    context = {
        'posts': posts,
        'advs': advs,
    }
    return render(request, "all-news.html", context)


def news_by_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    posts = Post.objects.filter(category=category).order_by('-created_at')
    advs = get_random_advs(4)
    context = {
        'category': category,
        'posts': posts,
        'advs': advs,
    }
    return render(request, "news-by-category.html", context)


def search_page(request):
    advs = get_random_advs(4)
    return render(request, "search.html", {'advs': advs})


def search_results(request):
    query = request.GET.get('q', '').strip()
    results = []
    if query:
        results = list(Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        ).order_by('-created_at'))
    advs = get_random_advs(4)
    context = {
        'query': query,
        'results': results,
        'advs': advs,
    }
    return render(request, "search-results.html", context)


def read_news_page(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # Похожие посты из той же категории (исключая текущий)
    related_posts = list(Post.objects.filter(category=post.category).exclude(pk=pk))
    related_posts = random.sample(related_posts, min(4, len(related_posts)))
    advs = get_random_advs(4)
    context = {
        'post': post,
        'related_posts': related_posts,
        'advs': advs,
    }
    return render(request, "read-news.html", context)
