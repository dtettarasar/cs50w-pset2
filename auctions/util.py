def save_listing(creator_user_id, l_title, l_description, l_start_bid, l_img_url, l_category):
    
    print("init save listing function from util.py")
    
    listing_data = {
        
        'creator': creator_user_id,
        'title': l_title,
        'description': l_description,
        'start_bid': l_start_bid,
        'img_url': l_img_url,
        'category': l_category,
        'creation_status': None,
        'error_msg': []
        
    }
    
    if listing_data["title"] == '':
        
        listing_data['error_msg'].append("error: no title")
        
    if listing_data["description"] == '':
        
        listing_data['error_msg'].append("error: no description")
        
    if listing_data["start_bid"] == '':
        
        listing_data['error_msg'].append("error: no starting bid")
     
    return listing_data