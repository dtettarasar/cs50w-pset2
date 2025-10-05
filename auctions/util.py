import re

from django.db import DatabaseError, IntegrityError

from .models import Listing
from .models import Category
from .models import Bid

def save_listing(creator_user_id, l_title, l_description, l_start_bid, l_img_url, l_category_id):
    
    print("init save listing function from util.py")
    
    listing_data = {
        
        'creator': creator_user_id,
        'title': l_title,
        'description': l_description,
        'start_bid_str': l_start_bid,
        'start_bid_float': None,
        'img_url': l_img_url,
        'category_id': l_category_id,
        'category_obj': None,
        'created': None,
        'listing_obj': None,
        'error_msg': []
        
    }
    
    url_pattern = r"^https?:\/\/(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&//=]*)\.(?:jpg|jpeg|png|gif|bmp|webp|svg)$"
    
    # Validation process
    if listing_data["title"] == '':
        
        listing_data['error_msg'].append("error: no title")
        
    if listing_data["description"] == '':
        
        listing_data['error_msg'].append("error: no description")
        
    if listing_data["start_bid_str"] == '':
        
        listing_data['error_msg'].append("error: no starting bid")
        
    else:
        
        try:
            
            listing_data['start_bid_float'] = float(listing_data['start_bid_str'])
            
        except ValueError:
            
            listing_data['error_msg'].append("error: starting bid is not valid")
            
    if listing_data['category_id']:
        
        try:
            
            listing_data['category_obj'] = Category.objects.get(pk=listing_data['category_id'])
        
        except Category.DoesNotExist:
            
            # this is redondant as default value is already None, but we can improve that part later
            listing_data['error_msg'].append("Selected category does not exist.")
            listing_data['category_obj'] = None
        
    # if the user provide an url for the image, make sure the url is valid
    if listing_data['img_url'] != '':
        
        test_valid_url = re.match(url_pattern, listing_data['img_url'])
        
        if test_valid_url == None:
            
            listing_data['error_msg'].append("error: image url is not valid")
            
    if len(listing_data['error_msg']) != 0:
        
        print("we cannot insert listing in database")
        listing_data['created'] = False
    
    else:
        
        # if no errors message, then conditions are valid, we can make an insert:
        print("conditions are valid we can insert listing in database")
        
        try:
            
            print("init insertion")
            
            listing = Listing (
                title = listing_data["title"],
                description = listing_data["description"],
                start_bid = listing_data['start_bid_float'],
                current_bid = listing_data['start_bid_float'],
                img_url = listing_data['img_url'],
                creator = listing_data['creator'],
                category = listing_data['category_obj'],
            )
            
            listing.save()
            
            listing_data['listing_obj'] = listing
            listing_data['created'] = True
            
            # print("listing: ")
            # print(listing)
            
        except IntegrityError as e:
            
            print(f"Integrity error: {e}")  # log technique
            listing_data['error_msg'].append("An error occurred while saving the data. Please try again later")
            listing_data['created'] = False
            
        except DatabaseError as e:
            
            print(f"Database error: {e}")  # log technique
            listing_data['error_msg'].append("A technical problem has occurred. Please try again later.")
            listing_data['created'] = False

    
    return listing_data

def get_active_listings():
    
    listings = Listing.objects.filter(status='open').select_related("creator", "category")
    
    return listings

def get_listing_by_id(listing_id):
    
    print("init get_listing_by_id")
    print(f"request data for listing: {listing_id}")
    
    try:
        listing = Listing.objects.get(pk=listing_id)
        return listing
    
    except Listing.DoesNotExist:
        print(f"⚠️ No listing found with id {listing_id}")
        return None
    
    except Listing.MultipleObjectsReturned:
        print(f"⚠️ Multiple listings found with id {listing_id} (shouldn’t happen!)")
        return None
    
def create_bid(user_obj, listing_id, new_price):
    
    bid_data = {
        
        'creator': user_obj,
        'listing_id': listing_id,
        'new_price_str': new_price,
        'new_price_float': None,
        'listing_obj': None,
        'created': None,
        'error_msg': []
        
    }
    
    print("init create_bid function")
    # print("data: ")
    # print(f"user_id: {bid_data['creator']}")
    # print(f"listing_id: {bid_data['listing']}")
    # print(f"new_price_str: {bid_data['new_price_str']}")
    
    bid_data['listing_obj'] = get_listing_by_id(bid_data['listing_id'])
    
    if bid_data['listing_obj'] != None:
        
        print("listing found")
        print(bid_data['listing_obj'])
        
        # bid_data['listing_obj'] = listing
        
        # check that the new price is received in a valid format
        try:
        
            bid_data['new_price_float'] = float(bid_data["new_price_str"])
        
        except ValueError:
        
            print("error: price value is not valid")
            bid_data['error_msg'].append("Error: the price is not valid")
            
        # make sure the new price is higher than the listing current bid
        
        if bid_data['new_price_float'] is not None:
            
            if bid_data['new_price_float'] <= 0:
                
                bid_data['error_msg'].append("Invalid bid: must be positive")
                
            elif bid_data['new_price_float'] <= bid_data['listing_obj'].current_bid:
                
                bid_data['error_msg'].append("New bid must be higher than current bid")
            
    else:
        
        bid_data['error_msg'].append("A technical problem has occurred. Please try again later.")
    
    if len(bid_data['error_msg']) != 0:
        
        print("we cannot insert bid in database")
        bid_data['created'] = False
        
    else:
        
        # if no errors message, then conditions are valid, we can make an insert:
        print("conditions are valid we can insert bid in database")
        
        try:
            
            print("init insertion")
            
            bid_to_insert = Bid (
                
                creator = bid_data['creator'],
                listing = bid_data['listing_obj'],
                value = bid_data['new_price_float'],
                
            )
            
            bid_to_insert.save()
            
            print("inserted bid:")
            print(bid_to_insert)
            
            bid_data['created'] = True
            
        except IntegrityError as e:
            
            print(f"Integrity error: {e}")  # log technique
            bid_data['error_msg'].append("An error occurred while saving the data. Please try again later")
            bid_data['created'] = False
            
        except DatabaseError as e:
            
            print(f"Database error: {e}")  # log technique
            bid_data['error_msg'].append("A technical problem has occurred. Please try again later.")
            bid_data['created'] = False
    
    return bid_data
    
def close_auction(user_obj, listing_id,):
    
    close_auction_data = {
        
        'creator': user_obj,
        'listing_id': listing_id,
        'listing_obj': None,
        'error_msg': [],
        'auction_is_closed': None,
        
    }
    
    print("init close auction function")
    
    print("user_obj:")
    print(close_auction_data['creator'])
    
    print("listing_id")
    print(close_auction_data['listing_id'])
    
    
    
    