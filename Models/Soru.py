from mongoengine import document, fields

__author__ = 'alpan'


class SubQuestion(document.EmbeddedDocument):
    comment = fields.StringField()
    soru = fields.StringField()
    answera = fields.StringField()
    answerb = fields.StringField()
    answerc = fields.StringField()
    answerd = fields.StringField()
    answere = fields.StringField()
    correctanswer = fields.StringField()
    answers = fields.ListField()


class Question(document.Document):
    name = fields.StringField()
    sound = fields.StringField()
    qs = fields.ListField(fields.EmbeddedDocumentField(SubQuestion))