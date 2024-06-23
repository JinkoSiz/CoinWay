from .models import Campaign
from django.shortcuts import render, get_object_or_404
from .models import Campaign
from .utils import searchCampaigns


# Create your views here.
def campaigns(request):
    campaigns, search_query = searchCampaigns(request)
    campaigns = campaigns.only('title', 'featured_image', 'description')
    context = {'html_name': 'Кампании', 'campaigns': campaigns}
    return render(request, 'campaigns/campaigns.html', context)


def campaign(request, pk):
    campaignObj = get_object_or_404(Campaign, id=pk)
    return render(request, 'campaigns/campaign.html', {'campaign': campaignObj})
