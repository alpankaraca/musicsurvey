from mongoengine import document, fields
from Models.User import User

__author__ = 'alpan'



class SubQuestion(document.Document):
    sound = fields.StringField()
    comment = fields.StringField()
    soru = fields.StringField()
    answera = fields.StringField()
    answerb = fields.StringField()
    answerc = fields.StringField()
    answerd = fields.StringField()
    answere = fields.StringField()
    correctanswer = fields.StringField()
    answers = fields.ListField()

class Answer(document.Document):
    user = fields.ReferenceField(User)
    subsoru = fields.ReferenceField(SubQuestion)
    cevap = fields.StringField()
    correct = fields.BooleanField()

class Question(document.Document):
    sound = fields.StringField()
    qs = fields.ListField(fields.ReferenceField(SubQuestion))
    ans = fields.ListField(fields.ReferenceField(Answer))