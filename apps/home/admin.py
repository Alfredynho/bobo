from django.contrib import admin

from .models import Autor, Libro

@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
	list_display = ['nombre', 'nacionalidad']

	class Meta:
		model = Autor


@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
	list_display = ['titulo', 'genero', 'autorLibro']

	class Meta:
		model = Libro