import requests
from requests.compat import quote_plus
from django.shortcuts import render
from bs4 import BeautifulSoup
from . import models

BASE_CRAIGSLIST_URL = "https://lima.craigslist.org/search/?query={}"
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'

# Create your views here.
def home(request):
    return render(request, 'base.html')

def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    final_url = BASE_CRAIGSLIST_URL.format(quote_plus(search))

    response = requests.get(final_url)
    data = response.text

    soup = BeutifulSoup(data, features='html.parser')
    post_listings = soup.find_all('a', {'class': 'result-row'})

    final_postings = []

    for post in post_listings:
        post_title = post.find(class='result-title').text
        post_url = post.find('a').get('href')

        if post.find(class='result-price'):
            post_price = post.find(class='result-price').text
        else:
            post_price = 'No tiene precio'

        if post.find(class='result-image').get('data-ids'):
            post_image = post.find(class='result-image').get('data-ids')[0]

        final_postings.append((post_title, post_url, post_price))


    # print(search)
    stuff_for_frontend = {
        'search': search,
        'final postigns': final_postings
    }
    return render(request, 'my_app/new_search.html', stuff_for_frontend)
