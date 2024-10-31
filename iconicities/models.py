from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext as _

class Stimulus(models.Model):
	term = models.CharField(max_length=50, verbose_name=_('Term'))
	file_name = models.CharField(max_length=50, verbose_name=_('Filename'))
	is_active = models.BooleanField(default=True, verbose_name=_('Is active'))
	is_control = models.BooleanField(default=False, verbose_name=_('Is control'))

	class Meta:
		verbose_name = _('Stimulus')
		verbose_name_plural = _('Stimuli')
	
	def __str__(self):
		return self.file_name

class Form(models.Model):
	
	class Sex(models.TextChoices):
		MALE = "Male", 'Hombre'
		FEMALE = "Female", 'Mujer'
		OTHER = "Other", 'No me identifico con estas opciones'
		NA = "N/A", 'Prefiero no responder'

	class PreferredLanguage(models.TextChoices):
		LSU = "LSU", 'LSU'
		SPANISH = "Spanish", 'Español'
		OTHER = "Other", 'No me identifico con estas opciones'
		NA = "N/A", 'Prefiero no responder'

	class Education(models.TextChoices):
		SCHOOL = "School", 'Escuela'
		FIRST_CYCLE = "First Cycle", 'Educación media básica (3º de liceo terminado o similar)'
		SECONDARY = "Secondary education", 'Educación media superior (6º de liceo terminado o similar)'
		TERTIARY = "Tertiary education", 'Educación terciaria (tecnicatura, diplomatura o grado universitario)'
		OTHER = "Other", 'No me identifico con estas opciones'
		NA = "N/A", 'Prefiero no responder'
	
	class Mode(models.IntegerChoices):
		ONLINE = 1, 'En línea'
		OFFLINE = 2, 'Fuera de línea'
		DEBUG = 3, 'Desarrollo'

	guid = models.CharField(primary_key=True, max_length=32)
	created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
	test_mode = models.IntegerField(choices=Mode.choices, verbose_name=_('Mode'))
	is_mobile = models.BooleanField(default=False, verbose_name=_('Is mobile'))
	browser = models.CharField(max_length=30, blank=True, null=True, verbose_name=_('Browser'))
	operating_system = models.CharField(max_length=30, blank=True, null=True, verbose_name=_('Operating system'))
	birthdate = models.CharField(max_length=4, verbose_name=_('Birthdate'))
	sex = models.CharField(max_length=10, choices=Sex.choices, verbose_name=_('Sex'))
	education = models.CharField(max_length=30, choices=Education.choices, verbose_name=_('Education'))
	preferred_language = models.CharField(max_length=20, choices=PreferredLanguage.choices, verbose_name=_('Preferred language'), default=PreferredLanguage.NA)
	lsu_fluency = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(7)], verbose_name=_('LSU fluency'))

	class Meta:
		verbose_name = _('Form')
		verbose_name_plural = _('Forms')

	def __str__(self):
		return self.guid

class Reply(models.Model):
	form = models.ForeignKey(Form, related_name='replies', on_delete=models.CASCADE, verbose_name=_('Form'))
	stimulus = models.ForeignKey(Stimulus, on_delete=models.CASCADE, verbose_name=_('Stimulus'))
	iconicity = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(7)], verbose_name=_('Iconicity'))
	rt = models.IntegerField(null=True, blank=True, verbose_name=_('Response time'))
	te = models.IntegerField(null=True, blank=True, verbose_name=_('Time elapsed'))

	class Meta:
		verbose_name = _('Reply')
		verbose_name_plural = _('Replies')
		unique_together = ('form', 'stimulus')
