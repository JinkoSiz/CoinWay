from .models import Project, Tag, Network
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import re


def paginateProjects(request, projects, results):
    page = request.GET.get('page')
    paginator = Paginator(projects, results)

    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        projects = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        projects = paginator.page(page)

    if paginator.num_pages > 10:
        leftIndex = (int(page) - 4)

        if leftIndex < 1:
            leftIndex = 1

        rightIndex = (int(page) + 5)

        if rightIndex > paginator.num_pages:
            rightIndex = paginator.num_pages + 1
    else:
        leftIndex = 1
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex, rightIndex)

    return custom_range, projects


def searchTags(request):
    tags = Tag.objects.distinct().all()

    return tags


def searchNetworks(request):
    networks = Network.objects.distinct().all()

    return networks


def searchProjects(request):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query').strip()

    criteria = [item.strip() for item in re.split('[ ,]+', search_query) if item.strip()]

    projects = Project.objects.distinct()
    if criteria:
        tag_queries = [Q(tags__name__icontains=item) for item in criteria]
        network_queries = [Q(networks__name__icontains=item) for item in criteria]

        query = Q()
        for q in tag_queries + network_queries:
            query |= q

        projects = projects.filter(query)

    return projects, search_query
