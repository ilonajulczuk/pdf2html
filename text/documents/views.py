from django.http import HttpResponse
from django.shortcuts import render

from documents.models import Document
from rest_framework import viewsets, permissions
from documents.serializers import DocumentSerializer
from rest_framework.decorators import api_view, permission_classes


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

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


@api_view()
@permission_classes([permissions.IsAuthenticated])
def display(request, num):
    doc = Document.objects.get(pk=num)
    if doc.html:
        context = {"generated_html": doc.html}
        return render(request, 'documents/display.html', context)
    else:
        return HttpResponse(status=404)


def home(request):
    context = {}
    if request.user.is_authenticated():
        docs = Document.objects.order_by('-id').filter(owner=request.user)
        context["docs"] = docs[:10]
    return render(request, 'documents/home.html', context)
