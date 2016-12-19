from django import forms
from django.forms import ModelForm
from download.models import Download

class DownloadForm(ModelForm):
	class Meta:
		model = Download
		fields = ['name', 'surname', 'email', 'affiliation', 'project_name', 'project_description']
