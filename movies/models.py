from django.db import models
from django.core.validators import FileExtensionValidator


class Movie(models.Model):
    title = models.CharField(max_length=200)
    video = models.FileField(
        upload_to="movie_videos",
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=["mp4", "avi", "mkv"])],
    )

    def __str__(self):
        return self.title
