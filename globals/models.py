from django.db import models
from accounts.models import CustomUser
from django.utils.html import format_html

# Create your models here.

class Game(models.Model):
    id = models.AutoField(primary_key=True)
    game_name = models.CharField(max_length=50, verbose_name='Nombre', default='', null=True)
    description = models.TextField(verbose_name='Descripcion',default='', null=True)
    rules = models.TextField(verbose_name="Reglas",default='', null=True)
    url = models.URLField(default='', null=True)
    category = models.CharField(max_length=50, verbose_name="Categoria", default='', null=True)
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
    score = models.IntegerField(default='0', null=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    date_played = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'scores'
        ordering = ['-score']
        get_latest_by = 'date_played'

    def __str__(self):
        return f'{self.user.username} -> {self.score}'

class DialogueCategory(models.Model):
    id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=50,verbose_name='Categoria',default='', null=True)
    description = models.TextField(verbose_name='Descripcion',default='', null=True)

    class Meta:
        db_table = 'dialogue_categories'
        verbose_name = 'Categoria de dialogo'
        verbose_name_plural = 'Categorias de dialogos'

    def __str__(self):
        return self.category_name

class Dialogue(models.Model):
    id = models.AutoField(primary_key=True)

    dialogue = models.TextField(verbose_name='Dialogo',default='', null=True)

    category = models.ForeignKey(DialogueCategory, on_delete=models.CASCADE, verbose_name='categoria')
    game = models.ForeignKey(Game,on_delete=models.CASCADE, verbose_name='juego')

    class Meta:
        db_table = 'dialogues'
        verbose_name = 'Dialogo'
        verbose_name_plural = 'Dialogos'
        ordering = ['game__game_name']
    
    def __str__(self):
        return f'{self.game.game_name}->{self.category.category_name}: {self.dialogue}'


class GlobalRank(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    score = models.IntegerField(default=0, null=True)

    class Meta:
        db_table = 'global_rank'
        ordering = ['-score']
    
    def __str__(self):
        return f'{self.user.username}->{self.score}'


class BugReport(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=10, default='', null=True, verbose_name='Usuario')
    subject = models.CharField(max_length=150, default='', null=True, verbose_name='Asunto')
    description = models.TextField(default='', null=True, verbose_name='Descripcion')
    image = models.ImageField(upload_to='reports/', null=True, default='')

    class Meta:
        db_table = 'bug_reports'

    def image_preview(self):
        if self.image:
            return format_html('<img src="{}" style="max-width: 200px; max-height: 200px;" />', self.image.url)
        return '(Sin imagen)'
    image_preview.short_description = 'Imagen'

