from mongoengine import document, fields

__author__ = 'alpan'


class SubQuestions(document.EmbeddedDocument):
    subq = fields.StringField()
    answers = fields.ListField()
    correctanswer = fields.StringField()

class Question(document.Document):
    name = fields.StringField()
    sound = fields.StringField()
    qs = fields.ListField(fields.EmbeddedDocumentField(SubQuestions))