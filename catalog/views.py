from django.shortcuts import render

# Create your views here.

from django.contrib.auth import mixins
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from graphene_file_upload.django import FileUploadGraphQLView
from rest_framework import generics

class TokenLoginRequiredMixin(mixins.LoginRequiredMixin):

    """A login required mixin that allows token authentication."""

    def dispatch(self, request, *args, **kwargs):
        """If token was provided, ignore authenticated status."""
        http_auth = request.META.get("HTTP_AUTHORIZATION")

        if http_auth and "JWT" in http_auth:
            pass
          
        elif not request.user.is_authenticated:
            return self.handle_no_permission()

        return super(mixins.LoginRequiredMixin, self).dispatch(
            request, *args, **kwargs)
      
class PrivateGraphQLView(TokenLoginRequiredMixin, FileUploadGraphQLView):

    """This view supports both token and session authentication."""
    
    authentication_classes = [
        SessionAuthentication,
        JSONWebTokenAuthentication,
        ]