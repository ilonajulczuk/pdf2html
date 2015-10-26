from documents.models import Document
from rest_framework import serializers


class DocumentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Document
        fields = ('id', 'title', 'created_at', 'file', 'html', 'status')
