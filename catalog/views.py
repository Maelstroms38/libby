from django.shortcuts import render, redirect
from django.conf import settings
from catalog.models import Book, Author, BookImage
from reviews.models import Review

# Create your views here.

def index(request):
    """View function for home page of site."""
    books = Book.objects.all()
    authors = Author.objects.all()
    reviews = Review.objects.all()
    images = BookImage.objects.all()

    for book in books:
        image = BookImage.objects.filter(book=book).first()
        if image:
            book.image = image

    context = {
        'books': books,
        'books_count': books.count(),
        'authors_count': authors.count(),
        'reviews_count': reviews.count(),
        'images_count': images.count(),
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)