from django.db import models
from django.db.models import (CASCADE, BooleanField, CharField, DateTimeField,
                              ForeignKey, Model, TextField)

from apps.users.models import User


class BaseModel(Model):
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True  # This model will not be created in the database


class Task(BaseModel):
    title = CharField(max_length=255)
    description = TextField(blank=True, null=True)
    completed = BooleanField(default=False)
    user = ForeignKey(User, on_delete=CASCADE, related_name="tasks")

    def __str__(self):
        return self.title
