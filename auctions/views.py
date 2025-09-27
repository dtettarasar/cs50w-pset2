from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
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
    
    print("accessing view listing page")
    
    listing = util.get_listing_by_id(listing_id)
    print(listing)
    
    return render(request, "auctions/view_listing.html", {
        'listing_id': listing_id,
        'listing': listing
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
