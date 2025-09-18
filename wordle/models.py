from django.db import models

# Create your models here.

class WordleWord(models.Model):
    id = models.AutoField(primary_key=True)
    word = models.CharField(max_length=12, null=False, unique=True, verbose_name = 'Palabra')
    

    class Meta:
        db_table = 'wordle_words'
    
    def __str__(self):
        return self.word
    
