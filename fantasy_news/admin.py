from django.contrib import admin
from .models import GameRecap


@admin.register(GameRecap)
class GameRecapAdmin(admin.ModelAdmin):
    list_display = ["title", "date"]
