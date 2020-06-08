from graphene import relay, ObjectType, Schema, Mutation, ID, Boolean
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.rest_framework.mutation import SerializerMutation
from catalog.api.serializers import BookSerializer
from catalog.filters import BookFilter
from catalog.models import Author, Book, BookImage
from graphene_file_upload.scalars import Upload
import boto3
import uuid

# AWS S3 "constants"
S3_BASE_URL = 's3.amazonaws.com' 
BUCKET = 'libby-app'

class BookImageNode(DjangoObjectType):
    class Meta:
        model = BookImage

class BookNode(DjangoObjectType):
    class Meta:
        model = Book
        interfaces = (relay.Node, )

class AuthorNode(DjangoObjectType):
    class Meta:
        model = Author
        filter_fields = []
        interfaces = (relay.Node, )

class Query(ObjectType):
    book = relay.Node.Field(BookNode)
    books = DjangoFilterConnectionField(BookNode, filterset_class=BookFilter)
    author = relay.Node.Field(AuthorNode)
    authors = DjangoFilterConnectionField(AuthorNode)


class BookMutation(SerializerMutation):
    class Meta:
        serializer_class = BookSerializer

class BookImageMutation(Mutation):
    class Arguments:
        file = Upload(required=True)
        id = ID(required=True)

    success = Boolean()

    def mutate(self, info, file, **data):
        # do something with your file
        # photo-file will be the "name" attribute on the <input type="file">
        photo_file = file
        book_id = data.get('id')
        if photo_file and book_id:
            s3 = boto3.client('s3')
            # need a unique "key" for S3 / needs image file extension too
            key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
            # just in case something goes wrong
            try:
                s3.upload_fileobj(photo_file, BUCKET, key)
                # build the full url string
                # url has to be unique, 
                # otherwise we risk overwriting existing files.
                url = f"https://{BUCKET}.{S3_BASE_URL}/{key}"
                # we can assign to book_id or book (if you have a book object)
                photo = BookImage(url=url, book_id=book_id)
                photo.save()
            except Exception as err:
                print('An error occurred uploading file to S3: %s' % err)
                return BookImageMutation(success=False)
        else: 
            print('Missing image or book ID')
            return BookImageMutation(success=False)

        return BookImageMutation(success=True)

class Mutation(ObjectType):
    book_mutation = BookMutation.Field()
    book_image_mutation = BookImageMutation.Field()

schema = Schema(query=Query, mutation=Mutation)