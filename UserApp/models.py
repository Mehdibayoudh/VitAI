from mongoengine import Document, StringField, EmailField, ImageField, BooleanField,DateTimeField
from django.contrib.auth.hashers import make_password, check_password
from django.db import models
from datetime import datetime


class User(Document):
    username = StringField(max_length=200, required=True, unique=True)
    email = EmailField(unique=True, required=True)
    password = StringField(required=True)
    image = ImageField()  # This field is optional, make it required if needed
    token = StringField()
    is_active = BooleanField(default=False)
    verification_token = StringField(max_length=64, blank=True, null=True)
    date_joined = DateTimeField(default=datetime.utcnow)

    def __str__(self):
        return self.username

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
