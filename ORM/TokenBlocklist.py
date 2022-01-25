from mongoengine import Document, StringField, IntField, DateTimeField

class TokenBlocklist(Document):
    jti = StringField(required=True, max_length=36)
    created_at = DateTimeField(null=False)