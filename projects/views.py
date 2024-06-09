from django.core import paginator
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Project, Tag, Tool
from .utils import searchProjects, paginateProjects, searchTags, searchNetworks


# Create your views here.

def projects(request):
    projects, search_query = searchProjects(request)
    tags = searchTags(request)
    networks = searchNetworks(request)
    custom_range, projects = paginateProjects(request, projects, 10000)

    context = {'projects': projects, 'search_query': search_query, 'custom_range': custom_range,
               'html_name': 'projects', 'tags': tags, 'networks': networks}
    return render(request, 'projects/projects.html', context)


def project(request, pk):
    projectObj = Project.objects.get(id=pk)

    return render(request, 'projects/single-project.html', {'project': projectObj, 'form': form})


def tools(request):
    tools = Tool.objects.all()
    context = {'tools': tools, 'html_name': 'tools'}

    return render(request, 'projects/tools.html', context)


def tool(request, pk):
    toolObj = Tool.objects.get(id=pk)

    return render(request, 'projects/single-tool.html', {'tool': toolObj})
