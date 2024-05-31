from django.db import models

from django.db import models
from django.contrib.auth.models import User

# Models for BD
class Subject(models.Model): # Book Django 2, page 304
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering=['title']

    def __str__(self):
        return self.title

class Course(models.Model):
    owner = models.ForeignKey(User, # преподаватель, который создал курс
                              related_name='courses_created',
                              on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, # предмет, к которому привязан курс
                                related_name='courses',
                                on_delete=models.CASCADE)
    title = models.CharField(max_length=200) # название курса
    slug = models.SlugField(max_length=200, unique=True) # слаг курса, будем использовать его для формирования
                                                        # человекопонятных url
    overview = models.TextField() # текстовое поле для создания краткого описания курса
    created = models.DateTimeField(auto_now_add=True) # дата и время создания курса

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title

class Module(models.Model):
    course = models.ForeignKey(Course,
                               related_name='modules',
                               on_delete=models.CASCADE
                               )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title

