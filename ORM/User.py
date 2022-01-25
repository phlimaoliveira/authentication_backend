from mongoengine import Document, StringField, EmailField

class User(Document):
    name = StringField(required=True, max_length=250)
    email = EmailField(required=True)
    password = StringField(required=True)