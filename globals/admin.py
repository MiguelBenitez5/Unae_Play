from django.contrib import admin
from .models import Game, DialogueCategory, Dialogue, BugReport
from django.contrib.admin.models import LogEntry

# Register your models here.

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('game_name','description','rules',)

@admin.register(Dialogue)
class DialogueAdmin(admin.ModelAdmin):
    list_display = ('dialogue','category','game')
    list_filter = ('category','game',)
    search_fields = ('dialogue', 'category__category_name','game__game_name')


@admin.register(DialogueCategory)
class DialogueCategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name','description')


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ("user", "content_type", "object_repr", "action_flag", "change_message", "action_time")
    list_filter = ("action_flag", "user", "content_type")
    search_fields = ("object_repr", "change_message")

@admin.register(BugReport)
class BugReportAdmin(admin.ModelAdmin):
    list_display = ('subject', 'description', 'image_preview')
