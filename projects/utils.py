from .models import Project, Tag, Network
from django.db.models import Q
import re


def searchTags(request):
    tags = Tag.objects.distinct().only('name').all()
    return tags


def searchNetworks(request):
    networks = Network.objects.distinct().only('name', 'featured_image').all()
    return networks


def searchProjects(request):
    search_query = request.GET.get('search_query', '').strip()
    criteria = [item.strip() for item in re.split('[ ,]+', search_query) if item.strip()]

    projects = Project.objects.distinct().only('title', 'featured_image', 'tags__name', 'networks__name')
    if criteria:
        query = Q()
        for item in criteria:
            query |= Q(tags__name__icontains=item) | Q(networks__name__icontains=item)
        projects = projects.filter(query).prefetch_related('tags', 'networks')

    return projects, search_query
