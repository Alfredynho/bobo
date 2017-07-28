from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Libro
class HomeView(TemplateView):
	template_name = "landing.html"

	def get_context_data(self, **kwargs):
		context = super(HomeView, self).get_context_data(**kwargs)
		context['libros'] = Libro.objects.all()
		return context