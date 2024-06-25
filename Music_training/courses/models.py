from django.db import models

from django.db import models
from django.contrib.auth.models import User

class Subject(models.Model):  # page 304
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta: # page 304
        ordering = ['title']

    def __str__(self): # page 304
        return self.title
class Course(models.Model): # page 304
    owner = models.ForeignKey(User,
                               related_name='courses_created',
                               on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject,
                                 related_name='courses',
                                 on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    students = models.ManyToManyField(User,  # page 354
                                      related_name='courses_joined', # page 354
                                      blank=True) # page 354
    class Meta: # page 304
        ordering = ['-created']
    def __str__(self): # page 304
        return self.title
from .fields import OrderField


class Module(models.Model): # page 304
    course = models.ForeignKey(Course,
                                related_name='modules',
                                on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = OrderField(blank=True, for_fields=['course'])  # page 314 поле сортировки в модели

    # def __str__(self): # page 304
    #     return self.title

    class Meta:
        ordering = ['order']

    def __str__(self):  # page 314
        return '{}. {}'.format(self.order, self.title)
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Content(models.Model): # page 308
    module = models.ForeignKey(Module,
                                related_name='contents',
                                on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType,  # page 312
                                     on_delete=models.CASCADE,
                                     limit_choices_to={'model__in': (
                                         'text',
                                         'video',
                                         'image',
                                         'file')})

    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    order = OrderField(blank=True, for_fields=['module'])  # page 315

    class Meta:
        ordering = ['order']


class ItemBase(models.Model): # page 311
    owner = models.ForeignKey(User,
                               related_name='%(class)s_related',
                               on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

class Text(ItemBase): # page 311
    content = models.TextField()

class File(ItemBase): # page 311
    file = models.FileField(upload_to='files')

class Image(ItemBase): # page 311
    file = models.FileField(upload_to='images')
# может быть не file а image ?

class Video(ItemBase): # page 311
    url = models.URLField()


