from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass

class Category(models.Model):
    
    cat_name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.id}: {self.cat_name}"
    
class Listing(models.Model):

    STATUS_CHOICES = [
        ("open", "Open"),
        ("closed", "Closed"),
        ("cancelled", "Cancelled"),
    ]

    title = models.CharField(max_length=64)
    description = models.TextField()
    start_bid = models.FloatField()
    current_bid = models.FloatField()
    img_url = models.URLField(max_length=500, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="open")

    # for the creator and winner : if we have to delete an user, we keep the related listing, we'll set the listing creator to null
    # make sure they have a related name so that 2 listing_sets can be created (as we have here to attributes related to the User model)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL,null=True,blank=True, related_name="created_listings")
    winner = models.ForeignKey(User, on_delete=models.SET_NULL,null=True,blank=True, related_name="won_listings")

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    
    # timestamps
    created_at = models.DateTimeField(auto_now_add=True) # set once at creation
    updated_at = models.DateTimeField(auto_now=True)      # updates every save()
    
    @property
    def formatted_bid(self):
        """Retourne le current_bid formaté en dollars"""
        if self.current_bid is not None:
            return "${:,.2f}".format(self.current_bid)
        return "No bid yet"
