from django.db import models

# Create your models here.

class WordleWord(models.Model):
    id = models.AutoField(primary_key=True)
    word = models.CharField(max_length=12, null=False, unique=True, verbose_name = 'Palabra')
    description = models.TextField(null=True,verbose_name='Descripción', blank=True)
    

    class Meta:
        db_table = 'wordle_words'
        verbose_name = 'Palabra'
        verbose_name_plural = 'Palabras'
    
    def __str__(self):
        return self.word
    

