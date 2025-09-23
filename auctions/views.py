from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User
from .models import Category

import re

from . import util

def index(request):
    return render(request, "auctions/index.html")


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
        # username = request.user.username
        # email = request.user.email

        print(f"user_id: {user_id}")
        # print(f"username: {username}")
        # print(f"email: {email}")
    
    else: 

        print("error user not authenticated")


    cat_list = Category.objects.all()
    # print("cat_list")
    # print(cat_list)
        
    if request.method == "POST":
        
        # TODO : insert all this code in external file
            
        print('post request received in create listing route')
        
        listing_data = util.save_listing(
            request.user.id,
            request.POST['listing-title'],
            request.POST['listing-description'],
            request.POST['listing-start-bid'],
            request.POST['listing-img'],
            request.POST['listing-cat'],
        )
        
        print("listing_data:")
        print(listing_data)

        listing_title = request.POST['listing-title']
        description = request.POST['listing-description']
        starting_bid = request.POST['listing-start-bid']
        starting_bid_float = None
        img_url = request.POST['listing-img']
        category = request.POST['listing-cat']

        print(f"listing_title: {listing_title}")

        # Validation process
        error_msg = []
        url_pattern = r"^https?:\/\/(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&//=]*)\.(?:jpg|jpeg|png|gif|bmp|webp|svg)$"

        if listing_title == '':

            print("error: no title")
            error_msg.append("error: no title")
        
        if description == '':

            print("error: no description")
            error_msg.append("error: no description")

        if starting_bid == '':

            print("error: no starting bid")
            error_msg.append("error: no starting bid")
        
        else:

            try:
                
                starting_bid_float = float(starting_bid)
            
            except ValueError:
                
                print("error: starting bid is not valid")
                error_msg.append("error: starting bid is not valid")

        # if the user provide an url for the image, make sure the url is valid
        if img_url != '':

            test_valid_url = re.match(url_pattern, img_url)

            if test_valid_url == None:

                error_msg.append("error: image url is not valid")


        # display the errors message if the form submission is not valid
        if len(error_msg) != 0:

            return render(request, 'auctions/create_listing.html', {
                "cat_list" : cat_list,
                "errors": error_msg
            })
            
        else: 
            
            # if no errors message, then conditions are valid, we can make an insert:
            
            print("conditions are valid we can insert listing in database") 
            print("listing_title")
            print(listing_title)
            print("---")
            print("description")
            print(description)
            print("---")
            print("starting_bid_float")
            print(starting_bid_float)
            print("---")
            print("img_url")
            print(img_url)
            print("---")
            print("category")
            print(category)
            print("---")

            # Si le process est valid. Pour le moment on redirige vers la page de la création de l'annonce, mais après, il faudra rediriger vers la page de la nouvelle annonce créée
            return render(request, 'auctions/create_listing.html', {
                "cat_list" : cat_list,
            })
            
    else:
        
        return render(request, 'auctions/create_listing.html', {
            "cat_list" : cat_list
        })
