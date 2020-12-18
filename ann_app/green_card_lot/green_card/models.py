from django.db import models

class PersonData(models.Model):
	login = models.CharField(max_length = 100)
	password = models.CharField(max_length = 100)
	form_01 = models.CharField(max_length = 400)
	form_02 = models.CharField(max_length = 400)
	form_03 = models.CharField(max_length = 400)
	form_04 = models.CharField(max_length = 400)
	form_05 = models.CharField(max_length = 400)
	form_06 = models.CharField(max_length = 400)
	form_07 = models.CharField(max_length = 400)
	form_08 = models.CharField(max_length = 400)
	form_09 = models.CharField(max_length = 400)
	form_10 = models.CharField(max_length = 400)
	form_11 = models.CharField(max_length = 400)
	form_12 = models.CharField(max_length = 400)
	form_13 = models.CharField(max_length = 400)

	def __str__(self):
		return f'id = {self.id}; {self.login}'

class LotteryEvent(models.Model):
	date = models.DateTimeField()
	winner_id = models.PositiveSmallIntegerField()

	def __str__(self):
		return f'id = {self.id}; date = {self.date}; winner_id = {self.winner_id}'