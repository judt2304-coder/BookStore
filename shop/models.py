from django.db import models
from django.contrib.auth.models import User

class Genre(models.Model):
    name = models.CharField("Жанр", max_length=100)

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField("Автор", max_length=200)

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField("Название книги", max_length=255)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name="Автор", related_name="books")
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Жанр", related_name="books")
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    pages = models.IntegerField("Количество страниц", default=200)
    cover_type = models.CharField("Переплёт", max_length=50, default="Твёрдый")
    image = models.ImageField("Обложка", upload_to="books/", blank=True, null=True)
    description = models.TextField("Описание", blank=True)
    is_promo = models.BooleanField("Акция", default=False)
    created_at = models.DateTimeField("Дата добавления", auto_now_add=True)

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} — {self.author.name}"


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь", related_name="favorites")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="Книга")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Избранное"
        verbose_name_plural = "Избранные книги"
        unique_together = ('user', 'book')


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь", related_name="cart_items")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="Книга")
    quantity = models.PositiveIntegerField("Количество", default=1)

    class Meta:
        verbose_name = "Товар в корзине"
        verbose_name_plural = "Товары в корзине"

    def get_total_price(self):
        return self.quantity * self.book.price


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    total_price = models.DecimalField("Итоговая сумма", max_digits=10, decimal_places=2, default=0)
    is_paid = models.BooleanField("Оплачено", default=False)
    created_at = models.DateTimeField("Дата заказа", auto_now_add=True)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField("Количество", default=1)
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Товар в заказе"
        verbose_name_plural = "Товары в заказе"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Заказ №{self.id} — {self.user.username}"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Заказ №{self.id} — {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.book.title} (x{self.quantity})"