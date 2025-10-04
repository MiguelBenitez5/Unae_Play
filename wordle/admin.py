from django.contrib import admin
from .models import WordleWord

# Register your models here.

@admin.register(WordleWord)
class WordleWordsAdmin(admin.ModelAdmin):
    list_display = ('word','description')
    search_fields = ('word',)