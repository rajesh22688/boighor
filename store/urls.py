from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("books/", views.books, name="books"),
    path("books/<int:book_id>/", views.book_detail, name="book_detail"),
    path("cart/", views.cart, name="cart"),
    path("cart/add/<int:book_id>/", views.add_to_cart, name="add_to_cart"),
    path( "cart/update/<int:item_id>/",views.update_cart,name="update_cart"),
    path("cart/remove/<int:item_id>/",views.remove_from_cart,name="remove_from_cart"),
    path("categories/", views.categories, name="categories"),
    path("contact/", views.contact, name="contact"),
    path("wishlist/", views.wishlist, name="wishlist"),
    path("orders/", views.orders, name="orders"),
    path("login/", views.login_view, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout_view, name="logout"),
    path("wishlist/add/<int:book_id>/",views.add_to_wishlist,name="add_to_wishlist"),
    path("wishlist/remove/<int:item_id>/",views.remove_from_wishlist,name="remove_from_wishlist"),
    path("checkout/",views.checkout,name="checkout"),
    path("payment-success/",views.payment_success,name="payment_success"),
    path("buy-now/<int:book_id>/",views.buy_now,name="buy_now"),
]
