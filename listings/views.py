from django.shortcuts import render, get_object_or_404
from .models import Listing
from .choices import price_choices, bedroom_choices, state_choices
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
def index(request):
    listings=Listing.objects.order_by('-list_date').filter(is_published=True)
    paginator= Paginator(listings,3)
    page=request.GET.get('page')
    paged_listings=paginator.get_page(page)
    context={
        'listings':paged_listings
    }
    return render(request, 'listings/listings.html', context=context)

def listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)

    context={
        "listing":listing
    }
    return render(request, 'listings/listing.html', context=context)

def search(request):
    query_filtered_listings= Listing.objects.order_by('-list_date')

    # For Keywords
    if 'keywords' in request.GET:
        keywords= request.GET['keywords']
        if keywords:
            query_filtered_listings=query_filtered_listings.filter(description__icontains=keywords)

    # For City
    if 'city' in request.GET:
        city= request.GET['city']
        if city:
            query_filtered_listings=query_filtered_listings.filter(city__iexact=city)

    # For State
    if 'state' in request.GET:
        state= request.GET['state']
        if state:
            query_filtered_listings=query_filtered_listings.filter(state__iexact=state)
    
    # For Bedrooms
    if 'bedrooms' in request.GET:   
        bedrooms= request.GET['bedrooms']
        if bedrooms:
            query_filtered_listings=query_filtered_listings.filter(bedrooms__lte=bedrooms)

    # For Prices
    if 'price' in request.GET:   
        price= request.GET['price']
        if price:
            query_filtered_listings=query_filtered_listings.filter(price__lte=price)

    context={
        "state_choices":state_choices,
        "bedroom_choices":bedroom_choices,
        "price_choices":price_choices,
        "listings": query_filtered_listings,
        "values": request.GET

    }
    return render(request, 'listings/search.html', context=context)

