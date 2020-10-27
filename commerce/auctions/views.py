from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User
from .models import Listings

def index(request):
    active_listings = Listings.objects.filter(is_sold=False)

    return render(request, "auctions/index.html", {
        "active_listings" : active_listings
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def listing_page(request, id):

    listing = Listings.objects.get(pk=id)

    return render(request, "auctions/individual_listing.html", {
        "listing" : listing
    })




def create_listing(request):
    if request.method == "GET":
        return render(request, "auctions/create_listing.html")
    elif request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        IMG_URL = request.POST["IMG_URL"]
        starting_price = request.POST["starting price"]
        current_price = request.POST["current price"]
        create_listing = Listings(title = title, description = description, IMG_URL = IMG_URL,
                         starting_price = starting_price, current_price = current_price, is_sold = 'True')
        create_listing.save()
        return render(request, "auctions/create_listing.html", {
        "message": "successfully added to db"
        })
