import re
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.http import JsonResponse
from .models import Book, Genre, Favorite, CartItem


def book_list(request):
    genres = Genre.objects.all()
    books = Book.objects.all()

    query = request.GET.get('q', '').strip()
    genre_id = request.GET.get('genre')
    genre_name = request.GET.get('genre_name')

    # Поиск (без учета регистра через iregex)
    if query:
        safe_query = re.escape(query)
        books = books.filter(
            Q(title__iregex=safe_query) |
            Q(author__name__iregex=safe_query) |
            Q(genre__name__iregex=safe_query)
        )

    # Фильтрация по ID жанра
    if genre_id:
        books = books.filter(genre_id=genre_id)

    # Фильтрация по названию жанра (для карточек внизу страницы)
    if genre_name:
        books = books.filter(genre__name__iregex=re.escape(genre_name))

    fav_ids = []
    if request.user.is_authenticated:
        fav_ids = Favorite.objects.filter(user=request.user).values_list('book_id', flat=True)

    return render(request, 'shop/book_list.html', {
        'books': books,
        'genres': genres,
        'fav_ids': fav_ids,
        'query': query,
        'selected_genre_name': genre_name
    })


def promotions(request):
    promo_books = Book.objects.filter(is_promo=True)
    return render(request, 'shop/promotions.html', {'books': promo_books})


def cart_detail(request):
    if not request.user.is_authenticated:
        return redirect('book_list')

    cart_items = CartItem.objects.filter(user=request.user).select_related('book')
    total_price = sum(item.get_total_price() for item in cart_items)

    return render(request, 'shop/cart.html', {'cart_items': cart_items, 'total_price': total_price})


def add_to_cart(request, book_id):
    if not request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'unauthorized', 'redirect_url': '/accounts/login/'}, status=401)
        return redirect('book_list')

    book = get_object_or_404(Book, id=book_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, book=book)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': 'ok'})

    return redirect(request.META.get('HTTP_REFERER', 'cart_detail'))


def remove_single_from_cart(request, book_id):
    if not request.user.is_authenticated:
        return redirect('cart_detail')

    try:
        cart_item = CartItem.objects.get(user=request.user, book_id=book_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except CartItem.DoesNotExist:
        pass

    return redirect('cart_detail')


def remove_from_cart(request, book_id):
    if not request.user.is_authenticated:
        return redirect('cart_detail')

    CartItem.objects.filter(user=request.user, book_id=book_id).delete()
    return redirect('cart_detail')


def toggle_favorite(request, book_id):
    if not request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'unauthorized', 'redirect_url': '/accounts/login/'}, status=401)
        return redirect('book_list')

    book = get_object_or_404(Book, id=book_id)
    fav, created = Favorite.objects.get_or_create(user=request.user, book=book)

    if not created:
        fav.delete()
        is_favorite = False
    else:
        is_favorite = True

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': 'ok', 'is_favorite': is_favorite})

    return redirect(request.META.get('HTTP_REFERER', 'book_list'))


def favorites_list(request):
    if not request.user.is_authenticated:
        return redirect('book_list')

    favorites = Favorite.objects.filter(user=request.user).select_related('book')
    return render(request, 'shop/favorites.html', {'favorites': favorites})


def checkout(request):
    if not request.user.is_authenticated:
        return redirect('book_list')

    CartItem.objects.filter(user=request.user).delete()
    return render(request, 'shop/checkout_success.html')

