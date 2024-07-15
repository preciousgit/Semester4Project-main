from django.db import models
from django.core.validators import FileExtensionValidator
from book_category.models import BookCategory
from movies.models import Movie


class Book(models.Model):
    BOOK_TYPE_CHOICES = [
        ("", "Please select book type"),  # Option for selection prompt
        ("book", "Book"),
        ("video", "Video"),
    ]

    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_date = models.DateField()
    isbn = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    downloadable = models.BooleanField(default=False)
    category = models.ForeignKey(BookCategory, on_delete=models.CASCADE, null=True)
    book_type = models.CharField(
        max_length=5, choices=BOOK_TYPE_CHOICES, default="", blank=True
    )

    # Image field for regular books
    image = models.ImageField(
        upload_to="book_images",
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png"])],
    )

    # Text file field for books with book_type 'txt'
    text_file = models.FileField(
        upload_to="book_text_files",
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=["txt"])],
    )

    # ForeignKey relationship with Movie model
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title
