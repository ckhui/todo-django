from django.db import models
from datetime import datetime

# Create your models here.
class Task(models.Model):
    title = models.TextField()
    date_created = models.DateTimeField(default=datetime.now)
    completed = models.BooleanField(default=False)

    editing = False

    def __str__(self):
        return self.title

    def class_name(self):
        c = []
        if self.completed:
            c.append('completed')

        if self.editing:
            c.append('editing')
            
        return "".join(c)

    def edit_title(self):
        return self.title

    def to_data(self):
        out = {}
        out['id'] = self.id
        out['title'] = self.title
        out['completed'] = self.completed
        return out
    