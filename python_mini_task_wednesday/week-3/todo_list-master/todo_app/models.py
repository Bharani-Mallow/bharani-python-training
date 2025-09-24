from django.urls import reverse
from django.db import models
from django.utils import timezone

def one_week_hence():
    return timezone.now() + timezone.timedelta(days=7)

class ToDoList(models.Model):
    title = models.CharField(max_length=100, unique=True)

    def get_absolute_url(self):
        return reverse('list', args=[self.id])

    def __str__(self):
        return self.title

class ToDoItem(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=300, null=True, blank=True)
    due_date = models.DateTimeField(default=one_week_hence)
    create_date = models.DateTimeField(auto_now_add=True)
    todo_list = models.ForeignKey(ToDoList, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('item_update', args=[str(self.todo_list.id), self.id])

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['due_date']
