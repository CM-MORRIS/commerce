from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django import forms
from datetime import date, datetime, timedelta

from .models import User
from .models import Listings

class ListingsForm(forms.Form):
    title = forms.CharField()
    # categories = forms.Charfield()
    description = forms.CharField()
    IMG_URL = forms.CharField()
    starting_price = forms.DecimalField()
    number_of_days = forms.IntegerField(min_value=3, max_value=7)

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

    if request.method == "POST":
        form = ListingsForm(request.POST)

        if form.is_valid():

            title           = form.cleaned_data["title"]
            description     = form.cleaned_data["description"]
            IMG_URL         = form.cleaned_data["IMG_URL"]
            starting_price  = form.cleaned_data["starting_price"]
            number_of_days  = form.cleaned_data["number_of_days"]
            end_date        = datetime.today() + timedelta(days=number_of_days)

            create_listing = Listings(title = title, description = description, IMG_URL = IMG_URL, starting_price = starting_price, current_price = starting_price, end_date = end_date)
            create_listing.save()

            return render(request, "auctions/create_listing.html", {

                "message": "successfully added to db"
            })

    else:
        return render(request, "auctions/create_listing.html", {
            "form": ListingsForm()
        })
