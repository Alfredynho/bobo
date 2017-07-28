from django.db import models


class Autor(models.Model):
	nombre = models.CharField(max_length=100)
	nacionalidad = models.CharField(max_length=100)

	def __str__(self):
		return self.nombre

class Libro(models.Model):
	titulo = models.CharField(max_length=100)
	genero = models.CharField(max_length=100)
	autor = models.ForeignKey(Autor)

	def __str__(self):
		return self.titulo

	def autorLibro(self):
		return self.autor