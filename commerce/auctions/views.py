from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django import forms
from datetime import date, datetime, timedelta
from .forms import ListingsForm, BiddingForm
from .models import User, Listings, Bids, Watchlist
from django.db.models import F
from django.contrib import messages



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

            # getting logged in user, 'request.user.id'
            current_user = User.objects.get(id=request.user.id)

            create_listing = Listings(title = title, user_id=current_user, description = description, IMG_URL = IMG_URL, starting_price = starting_price, current_price = starting_price, end_date = end_date)
            create_listing.save()

            return render(request, "auctions/create_listing.html", {
                "form": ListingsForm()
            })

    else:
        return render(request, "auctions/create_listing.html", {
            "form": ListingsForm()
        })


def listing_page(request, id):

    if request.method == "GET":

        try:
            listing = Listings.objects.get(pk=id)

        except Exception as e:
            print ("Error: " + str(e))
            print("Error: Listing page not found")
            return HttpResponseRedirect(reverse("index"))

        else:
            return render(request, "auctions/individual_listing.html", {
                "listing" : listing,
                "bid_form": BiddingForm()
            })


def bidding(request, id):

    # if bid is placed
    if request.method == "POST":

        bid_form = BiddingForm(request.POST)

        if bid_form.is_valid():

            new_bid_amount = bid_form.cleaned_data["new_bid"]

            listing = get_object_or_404(Listings, pk=id)

            current_price = listing.current_price

            # if bid valid add to db
            if new_bid_amount > current_price:

                # try add bid to db
                try:
                    # getting logged in user, 'request.user.id'
                    current_user = User.objects.get(id=request.user.id)

                    # adding users bid to db
                    new_bid_add = Bids(user_id=current_user, listing_id=listing, bid_price=new_bid_amount)

                    # updating listing current price to new bid amount
                    listing.current_price = new_bid_amount

                    # saving changes to db
                    new_bid_add.save()
                    listing.save()

                # if cannot get from db
                except Exception as e:
                    print ("Error: " + str(e))
                    return redirect('listing_page', id=id)

                # great success
                else:
                    messages.success(request, 'Your bid was successful!', extra_tags='alert alert-success')
                    return redirect('listing_page', id=id)

            # bid not valid
            else:
                messages.error(request, 'Bid too low! Please raise the amount', extra_tags='alert alert-danger')
                return redirect('listing_page', id=id)

        # if form not valid
        else:
            return redirect('listing_page', id=id)


    elif request.method == "GET":
        print("bidding view GET request")
        return redirect('listing_page', id=id)


def watchlist(request):

    # getting logged in user, 'request.user.id'
    # get_object_or_404 is equivalent to MyModel.objects.get
    current_user = get_object_or_404(User, id=request.user.id)

    # try add bid to db
    try:

        # This list contains a dictionary. With soley listing_ids
        # .values() returns a QuerySet that returns dictionaries, rather than model instances
        # .values_list() returns list
        watchlist_ids = Watchlist.objects.filter(user_id=current_user, is_on_list=True).values_list('listing_id')

        # extract all listings from table that exist in 'watchlist_ids' list -
        # us '__in' (listing_id__in) if filtering with a list (watchlist_ids)
        watchlist_listings = Listings.objects.filter(listing_id__in=watchlist_ids)

    except Exception as e:
        print ("Error: " + str(e))
        return render(request, "auctions/watchlist.html", { "watchlist_listings": None })

    # great success
    else:
        return render(request, "auctions/watchlist.html", { "watchlist_listings": watchlist_listings })


def add_to_watchlist(request, listing_id):

    # getting logged in user, 'request.user.id'
    current_user = get_object_or_404(User, id=request.user.id)

    listing_to_add = get_object_or_404(Listings, pk=listing_id)

    # if already on users watchlist, will go to exception 'Did not add to Watchlist'
    is_on_watchlist = Watchlist.objects.filter(user_id=current_user, listing_id=listing_id, is_on_list=True).exists()

    # if true, listing already in watchlist - redirect
    if is_on_watchlist:
        messages.error(request, 'Already in watchlist', extra_tags='alert alert-warning')
        return redirect('listing_page', id=listing_id)

    # try add to watchlist db
    try:
        add_listing_to_watchlist = Watchlist(user_id=current_user, listing_id=listing_to_add)
        add_listing_to_watchlist.save()

    # if cannot
    except Exception as e:
        print ("Error: " + str(e))
        messages.error(request, 'Did not add to Watchlist', extra_tags='alert alert-warning')
        return redirect('listing_page', id=listing_id)

    # great success
    else:
        print("else run - success")
        messages.success(request, 'Successfully added to Watchlist!', extra_tags='alert alert-success')
        return redirect('listing_page', id=listing_id)
