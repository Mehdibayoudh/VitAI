from mongoengine import Document, StringField, EmailField, ImageField, BooleanField
from django.contrib.auth.hashers import make_password, check_password


class User(Document):
    username = StringField(max_length=200)
    email = EmailField(unique=True)
    password = StringField()
    image = ImageField()
    token = StringField()
    verified = BooleanField(default=False)

    def __str__(self):
        return self.username

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
