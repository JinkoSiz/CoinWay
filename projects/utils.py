from .models import Project, Tag, Network
from django.db.models import Q
import re


def searchTags(request):
    return Tag.objects.only('name').all()


def searchNetworks(request):
    return Network.objects.only('name', 'featured_image').all()


def searchProjects(request):
    search_query = request.GET.get('search_query', '').strip()
    criteria = [item.strip() for item in re.split('[ ,]+', search_query) if item.strip()]

    projects = Project.objects.only('title', 'featured_image').prefetch_related('tags', 'networks')
    if criteria:
        query = Q()
        for item in criteria:
            query |= Q(tags__name__icontains=item) | Q(networks__name__icontains=item)
        projects = projects.filter(query).distinct()

    return projects, search_query
