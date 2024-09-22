from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import cache_page

from .models import Project, Tag, Tool
from .utils import searchProjects, searchTags, searchNetworks
from django.core.cache import cache
from django.conf import settings

# Время кэширования в секундах (можно задать для каждого типа данных)
CACHE_TTL = 60 * 15  # 15 минут


def projects(request):
    search_query = request.GET.get('query', '')

    # Кэширование только проектов
    cache_key = f"projects:{search_query}"
    cached_data = cache.get(cache_key)

    if not cached_data:
        projects, search_query = searchProjects(request)

        # Кэширование тегов и сетей отдельно
        tags = cache.get_or_set('tags', searchTags(request), CACHE_TTL)
        networks = cache.get_or_set('networks', searchNetworks(request), CACHE_TTL)

        # Оптимизация запросов к базе данных
        projects = projects.prefetch_related('tags', 'networks').only('title', 'featured_image', 'tags__name',
                                                                      'networks__name')

        cached_data = {
            'projects': projects,
            'search_query': search_query,
            'tags': tags,
            'networks': networks
        }

        # Сохранение в кэш
        cache.set(cache_key, cached_data, CACHE_TTL)

    # Извлекаем данные из кэша
    else:
        projects = cached_data['projects']
        search_query = cached_data['search_query']
        tags = cached_data['tags']
        networks = cached_data['networks']

    context = {
        'projects': projects,
        'search_query': search_query,
        'html_name': 'проекты',
        'tags': tags,
        'networks': networks
    }

    return render(request, 'projects/projects.html', context)


def project(request, pk):
    projectObj = get_object_or_404(Project, id=pk)
    return render(request, 'projects/single-project.html', {'project': projectObj})


# Оптимизация кэширования для инструментов
def tools(request):
    tools = cache.get_or_set('tools', Tool.objects.all().only('title', 'description'),
                             timeout=0)  # Долговременное кэширование
    context = {'tools': tools, 'html_name': 'Инструменты'}
    return render(request, 'projects/tools.html', context)


def tool(request, pk):
    cache_key = f"tool:{pk}"
    toolObj = cache.get(cache_key)

    if not toolObj:
        toolObj = get_object_or_404(Tool, id=pk)
        cache.set(cache_key, toolObj, CACHE_TTL)

    return render(request, 'projects/single-tool.html', {'tool': toolObj})


# Кэширование для новостей
@cache_page(CACHE_TTL)
def news(request):
    context = {'html_name': 'Новости'}
    return render(request, 'projects/news.html', context)
