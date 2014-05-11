# -*- coding: utf-8 -*-
import datetime
import os
from flask import Flask, redirect, render_template, request, url_for, session, current_app
from flask.ext.mongoengine import MongoEngine, MongoEngineSessionInterface
from flask.ext.mongomyadmin import MongoMyAdmin
from mongoengine import connect
from werkzeug.utils import secure_filename
from Models.User import User
from Models.Soru import Question, SubQuestion

app = Flask(__name__)
app.config.from_pyfile('appsettings.cfg')

connect(app.config.get("DB_NAME"), host='mongodb://' +app.config.get("DB_HOST_ADDRESS") )

m = MongoMyAdmin(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/god', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        if request.form['username'] == "alpan" and request.form['password'] == "gs1905":
            print "login tamam"
            session['username'] = request.form['username']
            return redirect(url_for('addquestion'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/addquestion', methods=["GET", "POST"])
def addquestion():
    if session.get("username") is None:
        return redirect("/god")

    if session.get("username") is "":
        return redirect("/god")

    if request.method == "POST":
        print "post"
        if request.args.get("audio"):
            print "upload"
            ALLOWED_EXTENSIONS = set(['mp3', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

            def allowed_file(filename):
                return '.' in filename and \
                       filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
            file = request.files['audio']
            import os
            if file and allowed_file(file.filename):
                print "dosya tipi doğru"
                s = Question()
                today = datetime.datetime.now().date()
                now = datetime.datetime.now().time()
                nowstr = str(now).split(":")
                newnow = nowstr[0] + "-" + nowstr[1]
                s.save()
                filename = str(s.id) + "-" + str(today) + "-" + str(newnow) + "-" + secure_filename(file.filename)
                file.save(os.path.join(os.path.abspath(os.path.dirname(__file__) + current_app.config['UPLOAD_FOLDER']), filename))
                s.sound = filename
                s.save()
                return render_template("addquestion.html", audio=filename, id=s.id)
            else:
                return "Yanlış dosya tipi"

        if request.args.get("addcommentquestion"):
            sound = Question.objects.get(id=request.args.get("addcommentquestion"))
            qs = sound.qs
            temp = qs
            soru = SubQuestion()
            soru.comment = request.form.get("commentsoru")
            temp.append(soru)
            sound.qs = temp
            sound.save()
            am = Question.objects.get(id=request.args.get("addcommentquestion")).qs
            return render_template("addquestion.html", audio=sound.sound, id=sound.id, qs=am)

        if request.args.get("addquestion"):
            sound = Question.objects.get(id=request.args.get("addquestion"))
            qs = sound.qs
            temp = qs
            soru = SubQuestion()
            soru.soru = request.form.get("soru")
            soru.answera = request.form.get("cevap-a")
            soru.answerb = request.form.get("cevap-b")
            soru.answerc = request.form.get("cevap-c")
            soru.answerd = request.form.get("cevap-d")
            soru.answere = request.form.get("cevap-e")
            soru.correctanswer = request.form.get("radio-cevap")
            temp.append(soru)
            sound.qs = temp
            sound.save()
            am = Question.objects.get(id=request.args.get("addquestion")).qs
            return render_template("addquestion.html", audio=sound.sound, id=sound.id, qs=am)
    return render_template('addquestion.html')



@app.route('/register', methods=["GET", "POST"])
def register():
    if request.args.get("age"):
        u = User()
        u.age = request.args.get("age")
        u.sex = request.args.get("sex")
        u.musician = request.args.get("musician")
        return redirect("/question")
    return render_template('register.html')

@app.route('/question', methods=["GET", "POST"])
def question():
    return render_template('question.html')

@app.errorhandler(404)
def not_found(error):
    return render_template('error.html'), 404

if __name__ == '__main__':
    print app.root_path
    app.run(host='0.0.0.0',debug=True)
