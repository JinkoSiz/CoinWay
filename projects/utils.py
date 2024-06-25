from .models import Project, Tag, Network
from django.db.models import Q
from django.core.cache import cache
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

    projects = Project.objects.all().only('id', 'title', 'featured_image', 'archive').prefetch_related('tags', 'networks')
    if criteria:
        query = Q()
        for item in criteria:
            query |= Q(tags__name__icontains=item) | Q(networks__name__icontains=item)
        projects = projects.filter(query)

    return projects, search_query


def get_cached_tags():
    tags = cache.get('tags')
    if not tags:
        tags = Tag.objects.distinct().only('name').all()
        cache.set('tags', tags, 60 * 60)  # Кэшировать на 1 час
    return tags


def get_cached_networks():
    networks = cache.get('networks')
    if not networks:
        networks = Network.objects.distinct().only('name', 'featured_image').all()
        cache.set('networks', networks, 60 * 60)  # Кэшировать на 1 час
    return networks
