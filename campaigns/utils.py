from .models import Campaign
from django.db.models import Q
import re


def searchCampaigns(request):
    search_query = request.GET.get('search_query', '').strip()
    criteria = [item.strip() for item in re.split('[ ,]+', search_query) if item.strip()]

    campaigns = Campaign.objects.distinct().only('title', 'featured_image', 'description')
    if criteria:
        query = Q()
        campaigns = campaigns.filter(query)

    return campaigns, search_query