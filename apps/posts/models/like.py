from django.conf import settings
from django.db import models

from .post import Post


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="likes"
    )

    class Meta:
        unique_together = ('user', 'post')  # нельзя лайкнуть дважды