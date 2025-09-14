from django.db import models
from accounts.models import CustomUser

# Create your models here.

class Game(models.Model):
    id = models.AutoField(primary_key=True)
    game_name = models.CharField(max_length=50)
    description = models.TextField()
    rules = models.TextField()
    url = models.URLField()
    category = models.CharField(max_length=50)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'games'
    
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

    def __str__(self):
        return self.user.username



