from django.contrib.auth.models import User
from django.db import models

LANGS = [
    ('py', 'Python'),
    ('js', 'JavaScript'),
    ('cpp', 'C++')
]


class Snippet(models.Model):
    name = models.CharField(verbose_name='Название', max_length=100)
    lang = models.CharField(verbose_name='Язык программирования', max_length=30, choices=LANGS)
    code = models.TextField(verbose_name='Код', max_length=5000)
    creation_date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Автор')
    public = models.BooleanField(verbose_name='Публичный', default=False)


class Comment(models.Model):
    text = models.TextField(max_length=2000)
    creation_date = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='Автор', related_name='comments')
    snippet = models.ForeignKey(to=Snippet, on_delete=models.CASCADE, verbose_name='Сниппет', related_name='comments')
