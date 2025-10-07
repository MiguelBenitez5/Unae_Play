from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # 'id', 'username', 'email', 'password' ya vienen por defecto
    email = models.EmailField(unique=True, verbose_name='Correo Electronico')  # asegura emails únicos
    age= models.IntegerField(verbose_name='edad', default=0, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'users'  

    def __str__(self):
        return self.username