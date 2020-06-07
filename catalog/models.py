from django.db import models

class Book(models.Model):
	title = models.CharField(max_length=200)
	# Foreign Key used because book can only have one author, but authors can have multiple books
	# Author as a string rather than object because it hasn't been declared yet in the file
	author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
	summary = models.TextField(max_length=1000, help_text='Enter a brief description of the book')

	class Meta:
		ordering = ['-id']

	def __str__(self):
		"""String to represent the model object"""
		return self.title

class BookImage(models.Model):
	book = models.ForeignKey(Book, on_delete=models.CASCADE)
	url = models.CharField(max_length=255)

	def __str__(self):
		return self.book.name or ""

	class Meta:
		verbose_name = "Book Image"
		verbose_name_plural = "Book Image"

class Author(models.Model):
	"""Model representing an author."""
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)

	class Meta:
		ordering = ['last_name', 'first_name']

	def __str__(self):
		"""String for representing the Model object."""
		return f'{self.last_name}, {self.first_name}'