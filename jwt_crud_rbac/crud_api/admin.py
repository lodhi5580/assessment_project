from django.contrib import admin
from .models import User, Book

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'role', 'is_active', 'date_joined')
    search_fields = ('username', 'email')
    list_filter = ('role', 'is_active', 'date_joined')

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'publication_date', 'edition', 'price')  # ✅ Fix "prise" → "price"
    search_fields = ('title', 'author__username')
    list_filter = ('publication_date',)


