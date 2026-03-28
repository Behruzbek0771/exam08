from django.db import models
from django.core.exceptions import ValidationError

from users.models import CustomUser


class Event(models.Model):
    class Event_Type(models.TextChoices):
        Online = 'ONLINE','Online'
        Offline = 'OFFLINE','Offline'

    title = models.CharField(max_length=180)
    description = models.TextField()
    event_type = models.CharField(choices=Event_Type.choices,max_length=10)
    location = models.CharField(max_length=50,null=True,blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    capacity = models.PositiveIntegerField()
    created_by = models.ForeignKey(CustomUser, verbose_name=("User event"), on_delete=models.CASCADE,related_name='event')

    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError('boshlanish vaqti tugash vaqtidan kichkina bo\'lishi kerak')
        
        if self.event_type == self.Event_Type.Offline and not self.location:
            raise ValidationError('Offline uchrashuvlar uchun location majburiy') 
        

    def __str__(self):
        return self.title

class Registration(models.Model):

    class Status(models.TextChoices):
        REGISTERED = "REGISTERED", "Registered"
        CANCELLED = "CANCELLED", "Cancelled"

    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="registrations")
    event = models.ForeignKey(Event,on_delete=models.CASCADE,related_name="registrations")
    status = models.CharField(max_length=15,choices=Status.choices,default=Status.REGISTERED)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "event"],
                name='bitta eventga bitta user yozila oladi'
            ),
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} -> {self.event} ({self.status})"