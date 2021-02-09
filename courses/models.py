from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from .fields import OrderField


class Subject(models.Model):
	title = models.CharField('Название', max_length=200)
	slug = models.SlugField(max_length=200, unique=True, verbose_name='Ссылка')

	class Meta:
		ordering = ['title']
		verbose_name = 'Предмет'
		verbose_name_plural = 'Предметы'

	def __str__(self):
		return self.title


class Course(models.Model):
	owner = models.ForeignKey(User, related_name='course_created', on_delete=models.CASCADE,
							  verbose_name='Преподаватель')
	subject = models.ForeignKey(Subject, related_name='courses', on_delete=models.CASCADE, verbose_name='Предмет')
	title = models.CharField('Название курса', max_length=200)
	slug = models.SlugField(max_length=200, unique=True, verbose_name='Ссыдка')
	overview = models.TextField('Краткое описание курса')
	created = models.DateTimeField('Создан', auto_now_add=True)

	class Meta:
		ordering = ['-created']
		verbose_name = 'Курс'
		verbose_name_plural = 'Курсы'

	def __str__(self):
		return self.title


class Module(models.Model):
	course = models.ForeignKey(Course, related_name='modules', on_delete=models.CASCADE, verbose_name='Курс')
	title = models.CharField('Название', max_length=200)
	description = models.TextField('Описание', blank=True)
	order = OrderField(blank=True, for_fields=['course'], verbose_name='Порядок')

	class Meta:
		verbose_name = 'Модуль'
		verbose_name_plural = 'Модули'
		ordering = ['order']

	def __str__(self):
		return f'{self.order}. {self.title}'


class Content(models.Model):
	module = models.ForeignKey(Module, related_name='contents', on_delete=models.CASCADE, verbose_name='Модуль')
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name='Тип контента',
									 limit_choices_to={'model__in': (
										 'text', 'video', 'image', 'file'
									 )})
	object_id = models.PositiveIntegerField('Идентификатор объекта (число)')
	item = GenericForeignKey('content_type', 'object_id')
	order = OrderField(blank=True, for_fields=['module'], verbose_name='Порядок')

	class Meta:
		verbose_name = 'Контент'
		verbose_name_plural = 'Контент'
		ordering = ['order']


class ItemBase(models.Model):
	owner = models.ForeignKey(User, related_name='%(class)s_related', on_delete=models.CASCADE,
							  verbose_name='Преподаватель')
	title = models.CharField('Название', max_length=250)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	class Meta:
		abstract = True

	def __str__(self):
		return self.title


class Text(ItemBase):
	content = models.TextField('Текст')


class File(ItemBase):
	file = models.FileField('Файл', upload_to='files')


class Image(ItemBase):
	file = models.FileField('Изображение', upload_to='images')


class Video(ItemBase):
	url = models.URLField('Ссылка на видео')
