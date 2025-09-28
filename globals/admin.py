from django.contrib import admin
from .models import Game, DialogueCategory, Dialogue

# Register your models here.

admin.site.register(Game)

admin.site.register(Dialogue)

admin.site.register(DialogueCategory)
