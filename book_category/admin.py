from django.contrib import admin
from .models import BookCategory


class BookCategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)


admin.site.register(BookCategory, BookCategoryAdmin)
