from rest_framework import serializers


class request_serializers(serializers.Serializer):
    user_url = serializers.CharField(required=True)
    number_words=serializers.IntegerField(required=False)