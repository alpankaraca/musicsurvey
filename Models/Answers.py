from mongoengine import document, fields
from Models.User import User
from Models.Soru import Question, SubQuestion

__author__ = 'alpan'


class Answer(document.Document):
    user = fields.ReferenceField(User)
    sound = fields.ReferenceField(Question)
    subsoru = fields.ReferenceField(SubQuestion)
    cevap = fields.StringField()
    correct = fields.BooleanField()
