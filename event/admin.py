from django.contrib import admin

from .models import Event,CustomUser,Registration

admin.site.register([Event,CustomUser,Registration])