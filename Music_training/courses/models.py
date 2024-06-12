from django.db import models
from django.contrib.auth.models import User

from .fields import OrderField


# from .fields import OrderField

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
    students = models.ManyToManyField(User,  # page 354 . Чтобы хранить сведения о том, в каких курсах участвуют студенты
                                      related_name='courses_joined',
                                      blank=True)

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
    order = OrderField(blank=True, for_fields=['course'])  # 314 поле сортировки

    class Meta: # page 315
        ordering = ['order']

    def __str__(self):
#        return self.title
        return '{}. {}'.format(self.order, self.title) # page 314


from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Content(models.Model): # page 311
    module = models.ForeignKey(Module,
                                related_name='contents',
                                on_delete=models.CASCADE)
#    content_type = models.ForeignKey(ContentType, # page 311
#                                on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, # page 312
                                     on_delete=models.CASCADE,
                                     limit_choices_to={'model__in':(
                                         'text',
                                         'video',
                                         'image',
                                         'file')})

    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    order = OrderField(blank=True, for_fields=['module']) # page 315

    class Meta:  # page 315
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

    # def __str__(self): # page 315 стерто
    #     return self.title # page 315 стерто

class Text(ItemBase):
    content = models.TextField()

class File(ItemBase):
    file = models.FileField(upload_to='files')

class Image(ItemBase):
    file = models.FileField(upload_to='images')

class Video(ItemBase):
    url = models.URLField()

from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

class ItemBase(models.Model): # page 360
# ...
    def render(self):
        return render_to_string('courses/content/{}.html'.format(
                    self._meta.model_name), {'item': self})


