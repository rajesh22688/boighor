from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Book,Category,CartItem,WishlistItem,Order,OrderItem,ContactMessage
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import razorpay
from django.conf import settings

def home(request):

    books = Book.objects.all().order_by("-created_at")[:8]

    categories = Category.objects.all()

    context = {
        "books": books,
        "categories": categories,
    }

    return render(
        request,
        "store/home.html",
        context
    )


def books(request):

    all_books = Book.objects.all().order_by("title")

    search_query = request.GET.get("search", "")
    category_id = request.GET.get("category", "")
    sort = request.GET.get("sort", "")

    # Search
    if search_query:
        all_books = all_books.filter(
            title__icontains=search_query
        ) | all_books.filter(
            author__icontains=search_query
        )

    # Category filter
    if category_id:
        all_books = all_books.filter(
            category_id=category_id
        )

    # Sorting
    if sort == "price_low":
        all_books = all_books.order_by("price")

    elif sort == "price_high":
        all_books = all_books.order_by("-price")

    elif sort == "newest":
        all_books = all_books.order_by("-created_at")

    elif sort == "name":
        all_books = all_books.order_by("title")

    categories = Category.objects.all().order_by("name")

    context = {
        "books": all_books,
        "categories": categories,
        "search_query": search_query,
        "selected_category": category_id,
        "selected_sort": sort,
    }

    return render(
        request,
        "store/books.html",
        context
    )


def categories(request):

    all_categories = Category.objects.all().order_by("name")

    context = {
        "categories": all_categories,
    }

    return render(
        request,
        "store/categories.html",
        context
    )


def contact(request):

    success = False

    if request.method == "POST":

        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        if name and email and subject and message:

            ContactMessage.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message
            )

            success = True

    return render(
        request,
        "store/contact.html",
        {
            "success": success
        }
    )

# Temporary pages
# We will replace these with real functionality later.


@login_required
def wishlist(request):

    wishlist_items = WishlistItem.objects.filter(
        user=request.user
    ).select_related("book")

    return render(
        request,
        "store/wishlist.html",
        {
            "wishlist_items": wishlist_items
        }
    )
    
@login_required
def add_to_wishlist(request, book_id):

    book = get_object_or_404(Book, id=book_id)

    WishlistItem.objects.get_or_create(
        user=request.user,
        book=book
    )

    return redirect("book_detail", book_id=book.id)
@login_required
def remove_from_wishlist(request, item_id):

    wishlist_item = get_object_or_404(
        WishlistItem,
        id=item_id,
        user=request.user
    )

    wishlist_item.delete()

    return redirect("wishlist")


@login_required
def cart(request):
    cart_items = CartItem.objects.filter(
        user=request.user
    ).select_related("book")

    grand_total = sum(
        item.book.price * item.quantity
        for item in cart_items
    )

    context = {
        "cart_items": cart_items,
        "grand_total": grand_total,
    }

    return render(request, "store/cart.html", context)


@login_required
def update_cart(request, item_id):
    cart_item = get_object_or_404(
        CartItem,
        id=item_id,
        user=request.user
    )

    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))

        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()

    return redirect("cart")


@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(
        CartItem,
        id=item_id,
        user=request.user
    )

    cart_item.delete()

    return redirect("cart")



@login_required
def orders(request):

    user_orders = Order.objects.filter(
        user=request.user
    ).prefetch_related(
        "items__book"
    ).order_by("-created_at")

    return render(
        request,
        "store/orders.html",
        {
            "orders": user_orders
        }
    )


def login_view(request):

    if request.user.is_authenticated:
        return redirect("home")

    error = ""

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("home")

        error = "Invalid username or password."

    return render(
        request,
        "store/login.html",
        {"error": error}
    )
    
def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    recommended_books = Book.objects.filter(
        category=book.category
    ).exclude(
        id=book.id
    ).order_by("-created_at")[:4]

    context = {
        "book": book,
        "recommended_books": recommended_books,
    }

    return render(request, "store/book_detail.html", context)

@login_required
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        book=book
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect("cart")

def register(request):

    if request.user.is_authenticated:
        return redirect("home")

    error = ""

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            error = "Passwords do not match."

        elif User.objects.filter(username=username).exists():
            error = "Username already exists."

        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            login(request, user)

            return redirect("home")

    return render(
        request,
        "store/register.html",
        {"error": error}
    )
    
def logout_view(request):
    logout(request)
    return redirect("home")

@login_required
def checkout(request):

    cart_items = CartItem.objects.filter(
        user=request.user
    ).select_related("book")

    if not cart_items.exists():
        return redirect("cart")

    total_amount = sum(
        item.book.price * item.quantity
        for item in cart_items
    )

    if request.method == "POST":

        order = Order.objects.create(
            user=request.user,
            total_amount=total_amount,
            status="Pending"
        )

        for item in cart_items:

            OrderItem.objects.create(
                order=order,
                book=item.book,
                quantity=item.quantity,
                price=item.book.price
            )

        # Razorpay client
        client = razorpay.Client(
            auth=(
                settings.RAZORPAY_KEY_ID,
                settings.RAZORPAY_KEY_SECRET
            )
        )

        # Amount is in paise
        razorpay_amount = int(total_amount * 100)

        razorpay_order = client.order.create({
            "amount": razorpay_amount,
            "currency": "INR",
            "receipt": f"order_{order.id}",
            "payment_capture": 1
        })

        return render(
            request,
            "store/payment.html",
            {
                "order": order,
                "razorpay_order": razorpay_order,
                "razorpay_key": settings.RAZORPAY_KEY_ID,
                "amount": razorpay_amount,
            }
        )

    return render(
        request,
        "store/checkout.html",
        {
            "cart_items": cart_items,
            "total_amount": total_amount,
        }
    )
    
@login_required
def payment_success(request):

    order_id = request.GET.get("order_id")
    payment_id = request.GET.get("payment_id")
    razorpay_order_id = request.GET.get("razorpay_order_id")
    razorpay_signature = request.GET.get("razorpay_signature")

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    client = razorpay.Client(
        auth=(
            settings.RAZORPAY_KEY_ID,
            settings.RAZORPAY_KEY_SECRET
        )
    )

    try:

        client.utility.verify_payment_signature({
            "razorpay_order_id": razorpay_order_id,
            "razorpay_payment_id": payment_id,
            "razorpay_signature": razorpay_signature
        })

        order.status = "Confirmed"
        order.save()

        CartItem.objects.filter(
            user=request.user
        ).delete()

        return redirect("orders")

    except razorpay.errors.SignatureVerificationError:

        order.status = "Cancelled"
        order.save()

        return redirect("cart")
    
    
@login_required
def buy_now(request, book_id):

    book = get_object_or_404(Book, id=book_id)

    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        book=book
    )

    if not created:
        cart_item.quantity = 1
        cart_item.save()

    return redirect("checkout")

