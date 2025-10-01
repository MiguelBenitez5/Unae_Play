from django.db import models
from accounts.models import CustomUser

# Create your models here.

class Game(models.Model):
    id = models.AutoField(primary_key=True)
    game_name = models.CharField(max_length=50, verbose_name='Nombre')
    description = models.TextField(verbose_name='Descripcion')
    rules = models.TextField(verbose_name="Reglas")
    url = models.URLField()
    category = models.CharField(max_length=50, verbose_name="Categoria")
    active = models.BooleanField(default=True, verbose_name="activo")

    class Meta:
        db_table = 'games'
        verbose_name = 'Juego'
        verbose_name_plural = 'Juegos'

    
    def __str__(self):
        return self.game_name


class Score(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    score = models.IntegerField()
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    date_played = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'scores'
        ordering = ['-score']
        get_latest_by = 'date_played'

    def __str__(self):
        return f'{self.user.username} -> {self.score}'

class DialogueCategory(models.Model):
    id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=50,verbose_name='Categoria')
    description = models.TextField(verbose_name='Descripcion')

    class Meta:
        db_table = 'dialogue_categories'
        verbose_name = 'Categoria de dialogo'
        verbose_name_plural = 'Categorias de dialogos'

    def __str__(self):
        return self.category_name

class Dialogue(models.Model):
    id = models.AutoField(primary_key=True)
    dialogue = models.TextField(verbose_name='Dialogo', unique=True)
    category = models.ForeignKey(DialogueCategory, on_delete=models.CASCADE, verbose_name='categoria')
    game = models.ForeignKey(Game,on_delete=models.CASCADE, verbose_name='juego')

    class Meta:
        db_table = 'dialogues'
        verbose_name = 'Dialogo'
        verbose_name_plural = 'Dialogos'
        ordering = ['game__game_name']
    
    def __str__(self):
        return f'{self.game.game_name}->{self.category.category_name}: {self.dialogue}'




