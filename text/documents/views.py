from django.http import HttpResponse
from django.shortcuts import render

from django.contrib.auth.models import User
from documents.models import Document
from rest_framework import viewsets, permissions
from documents.serializers import UserSerializer, DocumentSerializer
from rest_framework.decorators import api_view, authentication_classes, permission_classes


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class DocumentViewSet(viewsets.ModelViewSet):
    """
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = DocumentSerializer
    queryset = Document.objects

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        user = self.request.user
        return Document.objects.filter(owner=user)


@api_view()
@permission_classes([permissions.IsAuthenticated])
def display(request, num):
    doc = Document.objects.get(pk=num)
    if doc.html:
        return HttpResponse(doc.html, status=200)
    else:
        return HttpResponse(status=404)
