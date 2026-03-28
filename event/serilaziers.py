from rest_framework import serializers

from .models import Event,Registration
from users.serializers import UserDataSerilizer

class EventSerializers(serializers.ModelSerializer):
    created_by = UserDataSerilizer(read_only = True)
    class Meta:
        model = Event
        fields = ['title','description','event_type','location','start_time','end_time','capacity','created_by']


class EventRegistrSerailizers(serializers.ModelSerializer):
    class Meta:
        model = Registration
        exclude = '__all__'