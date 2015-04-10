from django.db import models

# Create your models here.


class Computer(models.Model):
	name = models.CharField(max_length=100, blank=False)
	model = models.CharField(max_length=100, blank=False)
	cost = models.PositiveIntegerField(blank=False, null=False)

	def __str__(self):
		return '{} {}'.format(self.name, self.model)