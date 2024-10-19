from mongoengine import Document, StringField, DateField, IntField

class SportEvent(Document):
    name = StringField(max_length=255, required=True)
    date = DateField(required=True)
    location = StringField(max_length=255, required=True)
    participants = IntField(required=True)

    def __str__(self):
        return self.name

    # Set the collection name using meta
    meta = {
        'collection': 'event'  # This will set the collection name to 'sport_events'
    }
