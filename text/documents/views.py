import logging
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect
from django.shortcuts import render
from rest_framework import viewsets, permissions

from rest_framework.decorators import api_view, permission_classes

from documents.models import Document, DocumentStatus
from documents.serializers import DocumentSerializer

logger = logging.getLogger(__name__)


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
        logger.info("Saving with user: %s", self.request.user)
        serializer.save(owner=self.request.user)


@api_view()
def display(request, num):
    doc = Document.objects.get(pseudoid=num)
    context = {}
    # TODO(att): add document title.
    if doc.html:
        context["generated_html"] = doc.html
        context["status"] = "ready"
    if doc.status == DocumentStatus.ERROR:
        context["status"] = "error"

    return render(request, 'documents/display.html', context)


def home(request):
    context = {}
    if request.user.is_authenticated():
        docs = Document.objects.order_by('-id').filter(owner=request.user)
        context["docs"] = docs[:10]
    return render(request, 'documents/home.html', context)


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = True
            user.save()
            new_user = authenticate(username=request.POST['username'],
                                    password=request.POST['password1'])
            login(request, new_user)
            return HttpResponseRedirect("/")
    else:
        form = UserCreationForm()
    return render(request, "documents/register.html", {
        'form': form,
    })


def loginview(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return HttpResponseRedirect("/")
    else:
        form = AuthenticationForm()
    return render(request, "documents/login.html", {
        'form': form,
    })