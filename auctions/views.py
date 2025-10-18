from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages

from .models import User
from .models import Category
from .models import WatchListItem

from . import util

def index(request):
    
    print("get access to index page")
    
    active_listings = util.get_active_listings()
    user_watchlist_ids = []
    
    # print("active_listing:")
    # print(active_listings)
    
    if request.user.is_authenticated:
        
        user_watchlist_ids = (
            request.user.created_watch_list_items
            .values_list("listing__id", flat=True)
        )
    
    return render(request, "auctions/index.html", {
        "active_listings": active_listings,
        "user_watchlist_ids": user_watchlist_ids,
    })

def view_listing(request, listing_id):
    
    # print("accessing view listing page")
    
    user_is_listing_creator = None
    listing_in_user_watchlist = None
    listing = None
    listing_comments = None
    
    
    if listing_id.isdigit():
        listing = util.get_listing_by_id(listing_id)
    
    # print(listing)
    
    if listing != None:
        
        if request.user.is_authenticated:
        
            print("verify if user is creator")
            print(listing.creator.id)
        
            if listing.creator.id == request.user.id:
            
                print("the user is the listing creator")
                user_is_listing_creator = True
            
            else:
            
                print("the user is not the listing creator")
                user_is_listing_creator = False
            
            
            print("verify if listing is in user watchlist")
            listing_in_user_watchlist = util.listing_in_user_watchlist(request.user.id, listing.id)
            
        
        print("retrieve comments for the listing")
        
        listing_comments = listing.related_comments.select_related("creator").order_by("-created_at")
        
        print("COMMENTS:", listing_comments)
        
    
    return render(request, "auctions/view_listing.html", {
        'listing_id': listing_id,
        'listing': listing,
        'user_is_listing_creator': user_is_listing_creator,
        'listing_in_user_watchlist': listing_in_user_watchlist,
        'listing_comments': listing_comments
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
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


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
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")
    
def create_listing(request):

    if request.user.is_authenticated:

        print("user is authenticated")

        user_id = request.user.id

        print(f"user_id: {user_id}")
    
    else: 

        print("error user not authenticated")


    cat_list = Category.objects.all()
        
    if request.method == "POST":
            
        print('post request received in create listing route')
        
        listing_data = util.save_listing(
            request.user,
            request.POST['listing-title'],
            request.POST['listing-description'],
            request.POST['listing-start-bid'],
            request.POST['listing-img'],
            request.POST['listing-cat'],
        )
        
        print("listing_data:")
        print(listing_data)


        # display the errors message if the form submission is not valid
        if len(listing_data['error_msg']) != 0:

            return render(request, 'auctions/create_listing.html', {
                "cat_list" : cat_list,
                "errors": listing_data['error_msg']
            })
            
        elif listing_data['created']: 
            
            print("listing successfully created, we can now redirect to the new listing page")
            print("new listing id: ")
            print(listing_data['listing_obj'].id)
            
            return redirect("auctions:view_listing", listing_id=listing_data['listing_obj'].id)
            
    else:
        
        return render(request, 'auctions/create_listing.html', {
            "cat_list" : cat_list
        })

def create_bid(request, listing_id):
    
    print("get access to create bid view")
    
    if request.user.is_authenticated:

        print("user is authenticated")

        user_id = request.user.id
        
        if request.method == "POST":
        
            print('post request received in create bid route')
            bid = util.create_bid(request.user, listing_id, request.POST['listing-new-bid'])
            print(bid)
            
            if bid['created']:
                messages.success(request, "✅ Your bid has been placed successfully!")
            else:
                for err in bid['error_msg']:
                    messages.error(request, f"❌ {err}")
    
    else: 

        print("error user not authenticated")
        messages.error(request, "❌ You must be logged in to place a bid.")
        
    return redirect("auctions:view_listing", listing_id=listing_id)

def close_auction(request, listing_id):
    
    print("get access to close auction view")
    
    if request.user.is_authenticated:

        print("user is authenticated")

        user_id = request.user.id
        
        if request.method == "POST":
        
            print('post request received in close auction route')
            
            close_auction_data = util.close_auction(request.user, listing_id)
            print('close_auction_data')
            print(close_auction_data)
    
    else: 

        print("error user not authenticated")
        messages.error(request, "❌ You must be logged in to close the auction.")
    
    return redirect("auctions:view_listing", listing_id=listing_id)


def add_to_watchlist(request, listing_id):
    
    print("get access to the add to watchlist view")
    
    if request.user.is_authenticated:

        print("user is authenticated")

        user_id = request.user.id
        
        if request.method == "POST":
        
            print('post request received in add to watchlist route')
            
            watchlist_data = util.add_to_watchlist(user_id, listing_id)
            
            print("watchlist_data: ")
            print(watchlist_data)
            
            print('request.POST.get("next")')
            print(request.POST.get("next"))
            
            next_url = request.POST.get("next") or reverse("auctions:index")
            
            return redirect(next_url)
    
    else: 

        print("error user not authenticated")
        messages.error(request, "❌ You must be logged in to add to watchlist.")
    
    return redirect("auctions:view_listing", listing_id=listing_id)


def remove_from_watchlist(request, listing_id):
    
    print("get access to the remove from watchlist view")
    
    if request.user.is_authenticated:

        print("user is authenticated")

        user_id = request.user.id
        
        if request.method == "POST":
        
            print('post request received in add to watchlist route')
            
            watchlist_data = util.remove_from_watchlist(user_id, listing_id)
            
            print("watchlist_data: ")
            print(watchlist_data)
            
            print('request.POST.get("next")')
            print(request.POST.get("next"))
            
            next_url = request.POST.get("next") or reverse("auctions:index")
            
            return redirect(next_url)
            
    else: 

        print("error user not authenticated")
        messages.error(request, "❌ You must be logged in to add to watchlist.")
    
    return redirect("auctions:view_listing", listing_id=listing_id)

def watchlist(request):
    
    print("get access to watchlist page")
    
    active_listings = util.get_active_listings()
    user_watchlist_ids = []
    
    user_watchlist = None
    
    # print("active_listing:")
    # print(active_listings)
    
    if request.user.is_authenticated:
        
        user_watchlist = WatchListItem.objects.filter(creator=request.user).select_related('listing')
        
        print("user watchlist")
        print(user_watchlist)
    
    return render(request, "auctions/watchlist.html", {
        "user_watchlist": user_watchlist,
    })