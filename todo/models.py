from django.db import models

class Todo(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False) # 완료 여부
    important = models.BooleanField(default=False) # 중요 여부

    def __str__(self):
        return self.title
