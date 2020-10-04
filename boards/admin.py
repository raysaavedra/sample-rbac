from django.contrib import admin

from .models import (
    Topic,
    Board,
    Thread,
    Post
)


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = [
        'id', 
        'name',
    ]


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = [
        'id', 
        'title',
        'admin',
        'topic'
    ]


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = [
        'id', 
        'title',
        'admin',
        'board'
    ]


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [
        'id', 
        'message',
        'user',
        'thread'
    ]
