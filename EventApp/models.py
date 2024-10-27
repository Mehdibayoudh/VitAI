from mongoengine import Document, StringField, DateField, IntField, ListField, ImageField

class SportEvent(Document):
    name = StringField(max_length=255, required=True)
    date = DateField(required=True)
    location = StringField(max_length=255, required=True)
    participants = IntField(required=True)
    AlreadyParticipated = IntField(default=0)  # Count of participants
    participants_list = ListField(StringField(), default=[])  # List of participant usernames or IDs
    owner = StringField(required=True)  # New field to track the owner's ID
    description = StringField()
    image = ImageField()

    def __str__(self):
        return self.name

    # Set the collection name using meta
    meta = {
        'collection': 'event'
    }
