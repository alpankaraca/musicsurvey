from mongoengine import document, fields

__author__ = 'alpan'

class User(document.Document):
    musician = fields.BooleanField()
    sex = fields.StringField()
    age = fields.StringField()
    answers = fields.ListField(fields.BooleanField())
    score = fields.IntField(default=0)
    yil = fields.IntField(default=0)