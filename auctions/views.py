from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User
from .models import Category

from . import util

def index(request):
    
    print("get access to index page")
    
    active_listings = util.get_active_listings()
    print("active_listing:")
    print(active_listings)
    
    return render(request, "auctions/index.html", {
        "active_listings": active_listings
    })

def view_listing(request, listing_id):
    
    # print("accessing view listing page")
    
    user_is_listing_creator = None
    
    if request.user.is_authenticated:

        # print("user is authenticated")

        user_id = request.user.id

        # print(f"user_id: {user_id}")
    
    # else: 

        # print("user not authenticated")
    
    listing = None
    
    
    if listing_id.isdigit():
        listing = util.get_listing_by_id(listing_id)
    
    # print(listing)
    
    if listing != None:
        
        print("verify if user is creator")
        print(listing.creator.id)
        
        if listing.creator.id == request.user.id:
            
            print("the user is the listing creator")
            user_is_listing_creator = True
            
        else:
            
            print("the user is not the listing creator")
            user_is_listing_creator = False
    
    return render(request, "auctions/view_listing.html", {
        'listing_id': listing_id,
        'listing': listing,
        'user_is_listing_creator': user_is_listing_creator
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
            
        else: 
            
            # Si le process est valid. Pour le moment on redirige vers la page de la création de l'annonce, mais après, il faudra rediriger vers la page de la nouvelle annonce créée
            return render(request, 'auctions/create_listing.html', {
                "cat_list" : cat_list,
            })
            
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
            print(f"listing_id: {listing_id}")
            print(f'new bid: {request.POST['listing-new-bid']}')
            print(f"user_id: {user_id}")
    
    else: 

        print("error user not authenticated")
        
    return redirect("auctions:view_listing", listing_id=listing_id)