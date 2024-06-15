from django.shortcuts import render, get_object_or_404
from .models import Project, Tag, Tool
from .utils import searchProjects, searchTags, searchNetworks
from django.views.decorators.cache import cache_page


@cache_page(60 * 15)  # Cache the view for 15 minutes
def projects(request):
    projects, search_query = searchProjects(request)
    tags = searchTags(request)
    networks = searchNetworks(request)

    projects = projects.prefetch_related('tags', 'networks').only('title', 'featured_image', 'tags__name', 'networks__name')

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
