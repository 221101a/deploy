from django.contrib import admin
from flight.models import *
# Register your models here.
admin.site.register(User)
admin.site.register(Profile)
admin.site.register(flights_from_to)
admin.site.register(fare)