from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext_lazy as _

from sample_rbac.models import BaseModel

User = get_user_model()


class Topic(BaseModel):
    name = models.CharField(_("Name of topic"), max_length=255)

    def __str__(self):
        return self.name


class Board(BaseModel):
    title = models.CharField(_("Title of Board"), max_length=255)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name="board_admins")
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="board_topics")
    moderators = models.ManyToManyField(User, blank=True, related_name="board_moderators")

    def generate_invite_url(self, user, request):
        return request.build_absolute_uri(f"{str(user.id)}/accept/")

    def __str__(self):
        return self.title


class Thread(BaseModel):
    title = models.CharField(_("Title of Board"), max_length=255)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name="thread_admins")
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="threads")

    def __str__(self):
        return self.title


class Post(BaseModel):
    message = models.TextField(_("Post message"))
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name="posts")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts_users")

    def __str__(self):
        return self.user.username
