from django.contrib import admin

# Register your models here.
from .models import Author, Book, BookImage

classes = [Author, Book, BookImage]

for model in classes:
	admin.site.register(model)