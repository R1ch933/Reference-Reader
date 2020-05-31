from django.db import models
from django.contrib.auth.models import User

# list of uploaded file names
class File_Name(models.Model):
    title = models.CharField(max_length=200)
    name = models.FileField()
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


