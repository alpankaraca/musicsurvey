from mongoengine import document, fields

__author__ = 'alpan'

class User(document.Document):
    musician = fields.BooleanField()
    sex = fields.BooleanField()
    age = fields.StringField()
    answers = fields.ListField()