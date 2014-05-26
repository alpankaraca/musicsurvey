# -*- coding: utf-8 -*-
import datetime
import json
import os
from flask import Flask, redirect, render_template, request, url_for, session, current_app
from flask.ext.mongoengine import MongoEngine, MongoEngineSessionInterface
from flask.ext.mongomyadmin import MongoMyAdmin
from mongoengine import connect
from werkzeug.utils import secure_filename
from Models import Answers
from Models.User import User
from Models.Soru import Question, Answer, SubQuestion

app = Flask(__name__)
app.config.from_pyfile('appsettings.cfg')

connect(app.config.get("DB_NAME"), host='mongodb://' + app.config.get("DB_HOST_ADDRESS") )

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
        if request.form['username'] == "nisan" and request.form['password'] == "123456_ooo":
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
    soundMaster = Question.objects.all()
    if session.get("username") is None:
        return redirect("/god")

    if session.get("username") is "":
        return redirect("/god")

    if request.method == "POST":
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
            soru.sound = request.args.get("addcommentquestion")
            soru.comment = request.form.get("commentsoru")
            soru.save()
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
            soru.sound = request.args.get("addquestion")
            soru.soru = request.form.get("soru")
            soru.answera = request.form.get("cevap-a")
            soru.answerb = request.form.get("cevap-b")
            soru.answerc = request.form.get("cevap-c")
            soru.answerd = request.form.get("cevap-d")
            soru.answere = request.form.get("cevap-e")
            at = request.form.get("radio-cevap")
            soru.correctanswer = request.form.get("cevap-"+at)
            soru.save()
            temp.append(soru)
            sound.qs = temp
            sound.save()
            am = Question.objects.get(id=request.args.get("addquestion")).qs
            return render_template("addquestion.html", audio=sound.sound, id=sound.id, qs=am)

        if request.args.get("delaudio"):
            id = request.args.get("delaudio")
            Question.objects.get(id=id).delete()
            return "Ses silindi"

        if request.args.get("delmulti"):
            print request.args.get("id")
            print int(request.args.get("delmulti"))-1
            #sound = Question.objects.get(id=id)
            #sound.qs.remove(sound.qs[count])
            #sound.save()
    return render_template('addquestion.html', sounds=soundMaster)



@app.route('/register', methods=["GET", "POST"])
def register():
    if request.args.get("age"):
        u = User()
        u.age = request.args.get("age")
        u.sex = request.args.get("sex")
        u.musician = json.loads(request.args.get("musician"))
        u.save()
        session['user'] = u.to_json()
        return redirect("/question")
    return render_template('register.html')

@app.route('/adilisik')
def adilisik():
    # remove the username from the session if it's there
    session.pop('user', None)
    return redirect(url_for('register'))


@app.route('/question', methods=["GET", "POST"])
def question():
    if request.args.get("sound"):
        print request.args.get("sound")
    if request.args.get("multi"):
        subq = request.args.get("multi")
        cevap = request.args.get("val")
        ses = request.args.get("ses")
        a = Answer()
        a.subsoru = SubQuestion.objects.get(id=subq)
        a.cevap = cevap
        corr = a.subsoru.correctanswer == cevap
        a.correct = corr
        user = User.objects.get(id=json.loads(session.get("user")).get("_id").get("$oid"))
        user.answers.append(corr)
        if corr:
            user.score += 10
        user.save()
        a.user = user
        a.save()
        sound = Question.objects.get(id=ses)
        sound.ans.append(a)
        sound.save()


    if request.args.get("comment"):
        subq = request.args.get("comment")
        cevap = request.args.get("val")
        ses = request.args.get("ses")
        a = Answer()
        a.subsoru = SubQuestion.objects.get(id=subq)
        a.sound = Question.objects.get(id=ses)
        a.cevap = cevap
        user = User.objects.get(id=json.loads(session.get("user")).get("_id").get("$oid"))
        a.user = user
        a.save()
        #print request.args.get("comment")



    soundMaster = Question.objects.all()
    return render_template('question.html', ses=soundMaster)



@app.route('/cevaplar', methods=["GET", "POST"])
def asnwers():
    if session.get("username") is None:
        return redirect("/god")

    if session.get("username") is "":
        return redirect("/god")

    if request.args.get("chart"):
        sound = Question.objects.get(id=request.args.get("chart"))
        for i in sound.ans:




    soundMaster = Question.objects.all()
    cevaplar = Answer.objects.all().order_by('question')
    return render_template('cevaplar.html', cevaplar=soundMaster, cinsiyet=["Erkek","Kadın"])


@app.errorhandler(404)
def not_found(error):
    return render_template('error.html'), 404

if __name__ == '__main__':
    print app.root_path
    app.run(host='0.0.0.0',debug=True, port=80)
