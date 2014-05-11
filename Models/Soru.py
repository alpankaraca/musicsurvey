from mongoengine import document, fields

__author__ = 'alpan'


class SubQuestion(document.EmbeddedDocument):
    soru = fields.StringField()
    answera = fields.StringField()
    answerb = fields.StringField()
    answerc = fields.StringField()
    answerd = fields.StringField()
    answere = fields.StringField()
    correctanswer = fields.StringField()
    comment = fields.StringField()


class Question(document.Document):
    name = fields.StringField()
    sound = fields.StringField()
    qs = fields.ListField(fields.EmbeddedDocumentField(SubQuestion))