from django.db import models

class Professors(models.Model):
	professor_name = models.CharField(max_length=140, primary_key=True, unique=True)
	url = models.URLField()
	overall_quality = models.FloatField()
	would_take_again = models.PositiveSmallIntegerField()
	level_of_difficulty = models.FloatField()
	hotness = models.CharField(max_length=20)

	def __str__(self):
		return self.professor_name
	

