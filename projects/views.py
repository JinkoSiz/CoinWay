from django.shortcuts import render, get_object_or_404
from .models import Project, Tag, Tool
from .utils import searchProjects, searchTags, searchNetworks, get_cached_tags, get_cached_networks
from django.views.decorators.cache import cache_page
from django.http import JsonResponse


@cache_page(60 * 15)  # Cache the view for 15 minutes
def projects(request):
    projects, search_query = searchProjects(request)
    tags = get_cached_tags()
    networks = get_cached_networks()

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


@cache_page(60 * 15)  # Cache the view for 15 minutes
def tools(request):
    tools = Tool.objects.all()
    context = {'tools': tools, 'html_name': 'Инструменты'}
    return render(request, 'projects/tools.html', context)


def tool(request, pk):
    toolObj = get_object_or_404(Tool, id=pk)
    return render(request, 'projects/single-tool.html', {'tool': toolObj})


@cache_page(60 * 15)  # Cache the view for 15 minutes
def news(request):
    context = {'html_name': 'Новости'}
    return render(request, 'projects/news.html', context)


def api_projects(request):
    try:
        projects, search_query = searchProjects(request)
        projects_data = [
            {
                'id': project.id,
                'title': project.title,
                'imageURL': project.imageURL,
                'tags': [tag.name for tag in project.tags.all()],
                'networks': [network.name for network in project.networks.all()],
                'archive': project.archive,
            }
            for project in projects
        ]
        return JsonResponse({'projects': projects_data})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

