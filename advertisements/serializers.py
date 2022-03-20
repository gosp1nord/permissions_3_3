from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Advertisement


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator', 'status', 'created_at', )

    def create(self, validated_data):
        """Метод для создания"""

        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""

        if self.context["request"].method == 'PATCH':
            count = 0
        else:
            count = 1
        for item in self.context["view"].queryset.values():
            if self.context["request"].user.id == item["creator_id"] and item['status'] == 'OPEN':
                count += 1
                if count == 11:
                    raise serializers.ValidationError('Нельзя держать открытыми более 10 объявлений.')
        return data

