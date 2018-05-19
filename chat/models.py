from django.db import models
from django.utils.text import slugify
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from contas.models import User


class Room(models.Model):
    objects = models.Manager
    name = models.TextField(max_length=50)
    label = models.SlugField(unique=True)

    def __str__(self):
        return self.label

    def save(self):
        self.label = slugify(self.name)
        super(Room, self).save()

    def get_absolute_url(self):
        return reverse_lazy('chat:room', kwargs={'label': self.label})

class Message(models.Model):
    objects = models.Manager
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return '[{timestamp}] {user}: {message}'.format(**self.as_dict())

    @property
    def formatted_timestamp(self):
        return self.created.strftime("%Y-%m-%d %H:%M:%S")

    def as_dict(self):
        return {'user': self.user.username, 'message': self.message, 'timestamp': self.formatted_timestamp}
