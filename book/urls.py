from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("index", views.index),
    path("books", views.books, name="books"),
    path('kitap-ekle', views.add_book, name='add-book'),
    path('make_trade_offer/<int:book_id>/', views.make_trade_offer, name='make_trade_offer'),
    path('accept_trade_offer/<int:offer_id>/', views.accept_trade_offer, name='accept_trade_offer'),
    path('trade_offers/', views.trade_offers, name='trade_offers'),
    path("category/<slug:slug>", views.books_by_category, name="books_by_category"),
    path("books/<slug:slug>", views.book_details, name="book_details"),
    path("all_trade_offers/", views.all_trade_offers, name="all_trade_offers"),
   


]