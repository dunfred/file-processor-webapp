from rest_framework import serializers
from .models import Document

class documentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = "__all__"


        