from django.contrib import admin
from .models import Books, Ratings

# Register your models here.
admin.site.register(Books)
admin.site.register(Ratings)