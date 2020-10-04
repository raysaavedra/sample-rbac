from rest_framework import serializers
from rolepermissions.roles import assign_role

from boards.models import (
    Topic,
    Board,
    Thread,
    Post
)
from users.api.v1.serializers import UserSerializer


class TopicSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Topic


class BoardSerializer(serializers.ModelSerializer):
    moderators = UserSerializer(many=True, read_only=True)
    admin = UserSerializer(read_only=True)
    
    class Meta:
        model = Board
        fields = (
            'title',
            'topic',
            'moderators',
            'admin'
        )

    def create(self, validated_data):
        user = self.context['request'].user

        assign_role(user, 'board_admin')

        return Board.objects.create(
            title=validated_data['title'],
            topic=validated_data['topic'],
            admin=user,
        )

    def save(self, request=None):
        return super().save()


class ThreadSerializer(serializers.ModelSerializer):
    admin = UserSerializer(read_only=True)
    
    class Meta:
        model = Thread
        fields = (
            'title',
            'board',
            'admin'
        )

    def create(self, validated_data):
        user = self.context['request'].user

        assign_role(user, 'thread_admin')

        return Thread.objects.create(
            title=validated_data['title'],
            board=validated_data['board'],
            admin=user,
        )

    def save(self, request=None):
        return super().save()


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = (
            'message',
            'thread',
        )

    def create(self, validated_data):
        return Post.objects.create(
            message=validated_data['message'],
            thread=validated_data['thread'],
            user=self.context['request'].user,
        )

    def save(self, request=None):
        return super().save()


class ModeratorInviteSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()

    class Meta:
        fields = (
            'user_id',
        )
        extra_kwargs = {
            'user_id': {
                'required': True
            },
        }
