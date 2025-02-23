from django.db import models
from users.models import CustomUser

class Feedback(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='feedbacks')
    comment = models.TextField()
    rating = models.PositiveSmallIntegerField()
    publish = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Feedback by {self.user.username} - {self.rating} Stars"