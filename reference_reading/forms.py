from django import forms
from .models import File_Name

#for uploading doc file
class UploadFileForm(forms.ModelForm):
    class Meta:
        model = File_Name
        fields = ['title', 'name']
        labels = {'title': 'Title', 'name': ''}