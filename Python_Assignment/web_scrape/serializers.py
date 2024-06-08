from rest_framework import serializers

class ScrapSerializer(serializers.Serializer):
    coins = serializers.ListField(
        child=serializers.CharField(max_length=100)
    )

class ScrapStatusSerializer(serializers.Serializer):
    job_id = serializers.CharField()