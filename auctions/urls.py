from django.urls import path

from . import views

app_name = 'auctions'

urlpatterns = [
    path("", views.index, name="index"),
    path("view-listing/<str:listing_id>/", views.view_listing, name="view_listing"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create-listing", views.create_listing, name="create_listing"),
    path("create-bid/<str:listing_id>/", views.create_bid, name="create_bid"),
    path("close-auction/<str:listing_id>/", views.close_auction, name="close_auction"),
    path("add-to-watchlist/<str:listing_id>/", views.add_to_watchlist, name='add_to_watchlist'),
    path("remove-from-watchlist/<str:listing_id>/", views.remove_from_watchlist, name='remove_from_watchlist'),
]
