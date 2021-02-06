from django.contrib import admin

from .models import Subject, Course, Module


@admin.register(Subject)
class AdminSubject(admin.ModelAdmin):
	list_display = ['title', 'slug']
	prepopulated_fields = {'slug': ('title',)}


class ModuleInline(admin.StackedInline):
	model = Module


@admin.register(Course)
class AdminCourse(admin.ModelAdmin):
	list_display = ['title', 'subject', 'created']
	list_filter = ['created', 'subject']
	search_fields = ['title', 'overview']
	prepopulated_fields = {'slug': ('title',)}
	inlines = [ModuleInline]
