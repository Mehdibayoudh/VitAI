from mongoengine import *
from django.contrib.auth.hashers import make_password, check_password
from django.db import models
from datetime import datetime


class User(Document):
    username = StringField(max_length=200, required=True, unique=True)
    email = EmailField(unique=True, required=True)
    password = StringField(required=True)
    token = StringField()
    is_active = BooleanField(default=False)
    verification_token = StringField(max_length=64, blank=True, null=True)
    date_joined = DateTimeField(default=datetime.utcnow)
    face_image = ImageField()  # Use MongoEngine's ImageField
    face_encodings = ListField()  # Store face encodings as a list of floats
    face_token = StringField(max_length=255, blank=True, null=True)  # Adjust length as needed
    face_dimensions = DictField()  # Store face dimensions as a dictionary
    feature_vector = ListField()  # Store feature vectors as a list of floats

    url = StringField(max_length=200, required=True, unique=True)

    def __str__(self):
        return self.username

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
