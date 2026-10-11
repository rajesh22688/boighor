from django.contrib import admin
from .models import (
    Category,
    Book,
    CartItem,
    WishlistItem,
    Order,
    OrderItem,
    ContactMessage,
)
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author",
        "category",
        "price",
        "language",
        "pages",
    )

    list_filter = (
        "category",
        "language",
    )

    search_fields = (
        "title",
        "author",
        "isbn",
        "publisher",
    )

    ordering = ("title",)
    
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("user", "book", "quantity")
    list_filter = ("user",)
    search_fields = ("user__username", "book__title")
    

@admin.register(WishlistItem)
class WishlistItemAdmin(admin.ModelAdmin):
    list_display = ("user", "book")
    search_fields = ("user__username", "book__title")
    
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "total_amount",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "created_at",
    )

    search_fields = (
        "user__username",
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        "order",
        "book",
        "quantity",
        "price",
    )

    search_fields = (
        "book__title",
        "order__user__username",
    )
    
    
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "email",
        "subject",
        "created_at",
    )

    search_fields = (
        "name",
        "email",
        "subject",
        "message",
    )

    ordering = ("-created_at",)