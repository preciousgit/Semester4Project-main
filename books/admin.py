from django.contrib import admin
from django.shortcuts import render
from django.urls import path
from django.utils.safestring import mark_safe
from .models import Book


class BookAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author",
        "publication_date",
        "isbn",
        "category",
        "book_type",  # Add book_type to list display
        "image_preview",
        "movie_details",
        "downloadable",
    )
    list_filter = (
        "author",
        "publication_date",
        "category",
        "book_type",
    )  # Add book_type to list filter
    search_fields = ("title", "author", "isbn", "category__name")
    readonly_fields = ("image_preview",)

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(
                '<img src="{url}" width="100" height="auto" />'.format(
                    url=obj.image.url
                )
            )
        else:
            return "(No image)"

    image_preview.short_description = "Image Preview"

    def save_model(self, request, obj, form, change):
        # Check if book type is "Please select book type"
        if obj.book_type == "":
            # If book type is not selected, prevent saving
            self.message_user(
                request, "Please select a valid book type.", level="ERROR"
            )
            return
        # Otherwise, allow saving
        super().save_model(request, obj, form, change)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        book_type_field = form.base_fields.get("book_type")
        if book_type_field:
            # If the book type is 'book', show the txt_file field
            if obj and obj.book_type == "book":
                txt_file_field = form.base_fields.get("txt_file")
                if txt_file_field:
                    txt_file_field.required = True
            # If the book type is 'video', hide the txt_file field
            elif obj and obj.book_type == "video":
                txt_file_field = form.base_fields.get("txt_file")
                if txt_file_field:
                    txt_file_field.required = False
                    form.base_fields.pop("txt_file")
        return form

    def movie_details(self, obj):
        if obj.movie:
            details = f"Title: {obj.movie.title}<br>"
            if obj.movie.video:
                details += (
                    f'<video width="320" height="240" controls>'
                    f'<source src="{obj.movie.video.url}" type="video/mp4">'
                    "Your browser does not support the video tag."
                    "</video>"
                )
            else:
                details += "(No video)"
            return mark_safe(details)
        else:
            return "(No movie selected)"

    movie_details.short_description = "Movie Details"

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path(
                "report/", self.admin_site.admin_view(self.report_view), name="report"
            ),
        ]
        return new_urls + urls

    def report_view(self, request):
        return render(request, "report.html", {"report_data": self.get_report_data()})

    def get_report_data(self):
        books = Book.objects.all()
        categories = books.values_list("category__name", flat=True).distinct()
        report_data = {}

        for category in categories:
            books_in_category = Book.objects.filter(category__name=category)
            report_data[category] = {
            "count": books_in_category.count(),
            "books": [{"name": book.title} for book in books_in_category]
            }
        return report_data


admin.site.register(Book, BookAdmin)
