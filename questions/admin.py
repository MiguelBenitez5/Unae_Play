from django.contrib import admin
from .models import Questions
# Register your models here.

@admin.register(Questions)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question','correct_answer',
                    'false_answer_1','false_answer_2',
                    'false_answer_3', 'question_info')
    search_fields = ('question',)