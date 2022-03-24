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
    creator = UserSerializer(read_only=True,)

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator', 'status', 'created_at', )

    def create(self, validated_data):
        """Метод для создания"""

        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""

        if self.context["request"].method == 'POST':
            if len(self.context["view"].queryset.filter(creator_id=self.context["request"].user.id, status='OPEN')) > 9:
                raise serializers.ValidationError('Нельзя держать открытыми более 10 объявлений.')
        elif self.context["request"].method == 'PATCH' and self.context["request"].data.get("status", False):
            creator_id = self.context["view"].queryset.filter(id=self.instance.id).values()[0]["creator_id"]
            if creator_id == self.context["request"].user.id:
                # если ты пытаешься изменить СВОЕ объявление
                if len(self.context["view"].queryset.filter(creator_id=self.context["request"].user.id, status='OPEN')) > 9 and self.context["request"].data.get("status") != "CLOSED":
                    raise serializers.ValidationError('Нельзя сделать открытыми более 10 объявлений.')
            else:
                # если пытаешься изменить ЧУЖОЕ объявление
                if len(self.context["view"].queryset.filter(creator_id=creator_id, status='OPEN')) > 9 and self.context["request"].data.get("status") != "CLOSED":
                    raise serializers.ValidationError('Нельзя сделать у другого пользователя открытыми более 10 объявлений.')
        return data


