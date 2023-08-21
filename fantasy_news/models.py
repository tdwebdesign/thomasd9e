from django.db import models


class GameRecap(models.Model):
    """
    Model to store game recaps scraped from ESPN.
    Each recap includes a date, title, body content, and a unique game ID.
    The 'processed' field indicates whether the recap has been used to create a story.
    """

    date = models.DateField()
    title = models.CharField(max_length=255)
    body = models.TextField()
    game_id = models.CharField(max_length=50, unique=True)
    processed = models.BooleanField(default=False, db_index=True)

    def __str__(self):
        return self.title
