from rest_framework import viewsets, permissions
from rest_framework.response import Response
from catalog.models import Author, Book
from catalog.api.serializers import AuthorSerializer, BookSerializer
from django_filters import rest_framework as filters
from catalog.filters import BookFilter

# 1. Define the viewset as a ModelViewSet
class AuthorViewSet(viewsets.ModelViewSet):
	# 2. Specify the queryset as "all authors"
    queryset = Author.objects.all()
    # 3. Assign the serializer class
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    """ 
  	 Returns a dictionary containing any extra context that should be supplied to the serializer. 
	 For more information, visit:
	 https://www.django-rest-framework.org/api-guide/generic-views/#customizing-the-generic-views
    """
    def get_serializer_context(self, *args, **kwargs):
        context = super(AuthorViewSet, self).get_serializer_context(*args, **kwargs)
        context['request'] = self.request
        return context

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = BookFilter
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]