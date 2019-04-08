from django.db import models
from datetime import datetime

# Create your models here.
class Task(models.Model):
    title = models.TextField()
    date_created = models.DateTimeField(default=datetime.now)
    completed = models.BooleanField(default=False)

    editing = True

    def __str__(self):
        return self.title

    def class_name(self):
        if self.editing:
            return 'editing'
        elif self.completed:
            return 'completed'
        else:
            return 'normal'

    def edit_title(self):
        return self.title
    