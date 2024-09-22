from django.shortcuts import render, get_object_or_404
from .models import Project, Tag, Tool
from .utils import searchProjects, searchTags, searchNetworks
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.conf import settings

# Время кэширования в секундах
CACHE_TTL = 60 * 15  # 15 минут


def projects(request):
    search_query = request.GET.get('query', '')

    # Генерируем уникальный ключ для кэша
    cache_key = f"projects:{search_query}"

    # Попытка получить кэшированные данные
    cached_projects = cache.get(cache_key)

    if not cached_projects:
        projects, search_query = searchProjects(request)
        tags = searchTags(request)
        networks = searchNetworks(request)

        # Оптимизация запросов к базе данных
        projects = projects.prefetch_related('tags', 'networks').only('title', 'featured_image', 'tags__name',
                                                                      'networks__name')

        cached_projects = {
            'projects': projects,
            'tags': tags,
            'networks': networks,
            'search_query': search_query
        }

        # Устанавливаем кэш с ключом и значением
        cache.set(cache_key, cached_projects, CACHE_TTL)
    else:
        # Если данные найдены в кэше, получаем их
        search_query = cached_projects['search_query']
        projects = cached_projects['projects']
        tags = cached_projects['tags']
        networks = cached_projects['networks']

    context = {
        'projects': projects,
        'search_query': search_query,
        'html_name': 'проекты',
        'tags': tags,
        'networks': networks
    }

    return render(request, 'projects/projects.html', context)


# Кэширование на уровне представления для "инструментов"
@cache_page(CACHE_TTL)  # Кэширование для 15 минут
def tools(request):
    tools = cache.get_or_set('tools', Tool.objects.all(), CACHE_TTL)
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
