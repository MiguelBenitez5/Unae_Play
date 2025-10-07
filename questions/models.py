from django.db import models

# Create your models here.
class Questions(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.CharField(max_length=191, blank=False, null=False, verbose_name='Pregunta')
    correct_answer = models.CharField(max_length=191, blank=False, null=False, verbose_name='Respuesta correcta')
    false_answer_1 = models.CharField(max_length=191, blank=False, null=False, verbose_name='Respuesta falsa')
    false_answer_2 = models.CharField(max_length=191, blank=False, null=False, verbose_name='Respuesta falsa')
    false_answer_3 = models.CharField(max_length=191, blank=False, null=False, verbose_name='Respuesta falsa')
    question_info = models.TextField(verbose_name='Informacion adicional')

    class Meta:
        db_table = 'questions'
        verbose_name = 'Pregunta'
        verbose_name_plural = 'Preguntas'
    
    def __str__(self):
        return f'{self.question}'
    
